from datetime import timezone
from rest_framework.response import Response
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from .serializers import GroupsSerializers, CategorySerializer, GroupBalanceSerializer
from .models import Groups, Category
from invitations.models import Family
from rest_framework.views import APIView
from django.db.models import Sum
from django.shortcuts import get_object_or_404
from transactions.models import Bank, Budget
from .models import Category
from collections import defaultdict
from django.utils import timezone




# Create your views here.
class GroupsCreateView(generics.ListCreateAPIView):
    serializer_class = GroupsSerializers
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        try:
            family = Family.objects.get(members=user)
            return Groups.objects.filter(family=family).prefetch_related('categories', 'family')
        except Family.DoesNotExist:
            return Groups.objects.none()

    def perform_create(self, serializer):
        family = Family.objects.get(members=self.request.user)
        serializer.save(groups_author=self.request.user, family=family)


class AddCategoryToGroupView(APIView):
    permission_classes = [IsAuthenticated]

    def get_group(self, pk):
        group = get_object_or_404(Groups, id=pk)
        if group.groups_author != self.request.user and group.family != self.request.user.family:
            raise PermissionError("You do not have permission to acces this groups")
        return group
    
    def get_group_queryset(self):
        return Groups.objects.filter(groups_author=self.request.user)
    
    def get(self, request, pk=None):
        if pk:
            group = self.get_group(pk)
            categories = group.categories.all()
        else:
            groups = self.get_group_queryset()
            categories = Category.objects.filter(groups__in=groups).distinct()
        
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, pk):
        # Dodawanie kategorii
        group = self.get_group(pk)
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            bank_id = request.data.get('bank')
            bank = Bank.objects.filter(id=bank_id).first() if bank_id else None
            category = serializer.save(category_author=self.request.user, bank=bank)
            group.categories.add(category)  # Add the new category to the group
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk, id):
        # Pełna aktualizacja kategorii
        group = self.get_group(pk)
        category = get_object_or_404(Category, id=id, group=group)
        serializer = CategorySerializer(category, data=request.data)
        if serializer.is_valid():
            bank_id = request.data.get('bank')
            bank = Bank.objects.filter(id=bank_id).first() if bank_id else None
            serializer.save(category_author=self.request.user, bank=bank)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk, id):
        # Częściowa aktualizacja kategorii
        group = self.get_group(pk)
        category = get_object_or_404(Category, id=id, group=group)
        serializer = CategorySerializer(category, data=request.data, partial=True)
        if serializer.is_valid():
            bank_id = request.data.get('bank')
            bank = Bank.objects.filter(id=bank_id).first() if bank_id else None
            serializer.save(category_author=self.request.user, bank=bank)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class GroupBalanceView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk=None):

        family = request.user.family
        # Możemy dodać filtry, np. tylko dla grup należących do zalogowanego użytkownika
        if pk:

            try:
                group = Groups.objects.get(id=pk, family=family)
                if group.groups_author != request.user and group.family != request.user.family:
                    return Response({"detail": "You do not have permission to view this group."}, status=status.HTTP_403_FORBIDDEN)
                serializer = GroupBalanceSerializer(group)
                return Response(serializer.data)
            except Groups.DoesNotExist:
                return Response({'detail': 'Group not found'}, status=status.HTTP_404_NOT_FOUND)
        else:
            # Jeśli nie podano `pk`, możemy zwrócić bilans dla wszystkich grup
            groups = Groups.objects.filter(family=family)
            serializer = GroupBalanceSerializer(groups, many=True)
            return Response(serializer.data)
        
class GroupBalanceForChartView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Pobieramy wszystkie grupy, do których użytkownik ma dostęp
        groups = Groups.objects.filter(groups_author=request.user) | Groups.objects.filter(family=request.user.family)

        # Jeśli użytkownik nie ma żadnych grup, zwrócimy odpowiedź z pustymi danymi
        if not groups.exists():
            return Response({"detail": "You do not belong to any group."}, status=status.HTTP_404_NOT_FOUND)

        # Zmienna do przechowywania danych dla wszystkich grup
        all_dates = []
        all_expenses = []

        # Iterujemy po grupach
        for group in groups:
            # Sprawdzamy, czy użytkownik jest autorem grupy lub należy do tej samej rodziny
            if group.groups_author != request.user and group.family != request.user.family:
                continue  # Jeśli użytkownik nie ma dostępu do grupy, pomijamy ją

            categories = group.categories.filter(category_type='expense')
            expenses_by_date = defaultdict(float)

            # Zbieramy wydatki z kategorii
            for category in categories:
                category_date = category.created_at.strftime("%Y-%m-%d")
                expenses_by_date[category_date] += category.assigned_amount

            # Dodajemy daty i wydatki z bieżącej grupy do list
            dates = list(expenses_by_date.keys())
            expenses = list(expenses_by_date.values())

            all_dates.extend(dates)
            all_expenses.extend(expenses)

        # Opcjonalnie: Sortowanie dat i wydatków
        sorted_data = sorted(zip(all_dates, all_expenses), key=lambda x: x[0])
        sorted_dates, sorted_expenses = zip(*sorted_data)

        # Zwracamy dane
        data = {
            "dates": sorted_dates,
            "expenses": sorted_expenses,
        }

        return Response(data, status=status.HTTP_200_OK)




class PreviousMonthBalanceView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        now = timezone.now()
        current_year = now.year
        current_month = now.month

        # Ustalamy poprzedni miesiąc
        if current_month == 1:
            previous_month = 12
            year = current_year - 1
        else:
            previous_month = current_month - 1
            year = current_year

        # Pobieramy dane z poprzedniego miesiąca
        total_balance = Budget.objects.filter(
            created_at__year=year,
            created_at__month=previous_month,
            family_id=request.user.family
        ).aggregate(total=Sum('amount'))['total'] or 0

        return Response({
            "year": year,
            "month": previous_month,
            "total_balance": total_balance
        })

class GroupCategoryDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get_group(self, group_id):
        """
        Pobiera grupę na podstawie ID i sprawdza, czy użytkownik ma do niej dostęp.
        """
        group = get_object_or_404(Groups, id=group_id)
        if group.groups_author != self.request.user and group.family != self.request.user.family:
            raise PermissionError("You do not have permission to access this group.")
        return group

    def get_category(self,group, category_id):
        return get_object_or_404(group.categories, id=category_id)

    def get(self, request, group_id, category_id):
        """
        Pobiera jedną kategorię z grupy na podstawie jej ID.
        """
        group = self.get_group(group_id)
        category = get_object_or_404(group.categories, id=category_id)
        serializer = CategorySerializer(category)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, group_id, category_id):
        group = self.get_group(group_id)
        # Correctly call get_category method to get the Category instance
        category = self.get_category(group, category_id)
        serializer = CategorySerializer(category, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, group_id, category_id):
        group = self.get_group(group_id)
        category = self.get_category(group, category_id)
        serializer = CategorySerializer(category, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, group_id, category_id):
        """
        Usuwa kategorię z grupy na podstawie jej ID.
        """
        group = self.get_group(group_id)
        category = self.get_category(group, category_id)
        category.delete()
        return Response({"detail": "Category deleted successfully."}, status=status.HTTP_204_NO_CONTENT)