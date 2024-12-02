from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import SavingsGoal
from .serializers import SavingsGoalSerializer
from rest_framework.permissions import IsAuthenticated

class SavingsGoalListCreateView(APIView):
    permission_classes = [IsAuthenticated]  # Upewnij się, że użytkownik jest uwierzytelniony

    def get(self, request):
        """
        Pobiera cele oszczędności przypisane do aktualnie zalogowanego użytkownika.
        """
        goals = SavingsGoal.objects.filter(user=request.user)
        serializer = SavingsGoalSerializer(goals, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        """
        Creates or updates a savings goal with a title.
        """
        request.data['user'] = request.user.id

        serializer = SavingsGoalSerializer(data=request.data)
        if not serializer.is_valid():
            print(f"Validation errors: {serializer.errors}")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        title = serializer.validated_data['title']
        goal_type = serializer.validated_data['goal_type']
        target_amount = serializer.validated_data['target_amount']
        current_amount = serializer.validated_data.get('current_amount', 0)

        print(f"Creating or updating goal: Title={title}, Goal Type={goal_type}, Target={target_amount}, Current={current_amount}")

        # Check if a goal with the same title and type exists
        goal, created = SavingsGoal.objects.get_or_create(
            user=request.user,
            title=title,
            goal_type=goal_type,
            defaults={
                'target_amount': target_amount,
                'current_amount': current_amount,
                'due_date': serializer.validated_data['due_date'],
            }
        )

        if not created:  # If the goal exists, update the `current_amount`
            if current_amount <= 0:
                print("Error: Amount to add must be greater than zero.")
                return Response(
                    {"detail": "Amount to add must be greater than zero."},
                    status=status.HTTP_400_BAD_REQUEST
                )
            goal.current_amount += current_amount
            goal.save()
            print("Existing goal updated.")
            message = "Existing goal updated successfully."
        else:
            print("New goal created.")
            message = "New goal created successfully."

        response_data = SavingsGoalSerializer(goal).data
        response_data['message'] = message
        print(f"Response data: {response_data}")

        return Response(response_data, status=status.HTTP_201_CREATED)




class SavingsGoalDetailView(APIView):

    def get_goal(self, pk, user):
        """Pomocnicza funkcja do pobierania celu"""
        try:
            return SavingsGoal.objects.get(pk=pk, user=user)
        except SavingsGoal.DoesNotExist:
            return None

    def get(self, request, pk):
        goal = self.get_goal(pk, request.user)
        if not goal:
            print(f"Goal with pk={pk} not found for user {request.user.id}")
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = SavingsGoalSerializer(goal)
        print(f"Goal data retrieved: {serializer.data}")
        return Response(serializer.data)

    def put(self, request, pk):
        goal = self.get_goal(pk, request.user)
        if not goal:
            print(f"Goal with pk={pk} not found for user {request.user.id}")
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = SavingsGoalSerializer(goal, data=request.data)
        if serializer.is_valid():
            serializer.save()
            print(f"Goal updated: {serializer.data}")
            return Response(serializer.data)
        print(f"Serializer errors: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        goal = self.get_goal(pk, request.user)
        if not goal:
            print(f"Goal with pk={pk} not found for user {request.user.id}")
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)

        goal.delete()
        print(f"Goal with pk={pk} deleted for user {request.user.id}")
        return Response(status=status.HTTP_204_NO_CONTENT)

    def patch(self, request, pk):
        goal = self.get_goal(pk, request.user)
        if not goal:
            print(f"Goal with pk={pk} not found for user {request.user.id}")
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)

        # Sprawdzamy, czy podano kwotę do dodania
        amount_to_add = request.data.get("current_amount", None)

        if amount_to_add and amount_to_add > 0:
            goal.current_amount += amount_to_add
            goal.save()
            return Response(SavingsGoalSerializer(goal).data, status=status.HTTP_200_OK)
        else:
            return Response({"detail": "Amount to add must be greater than zero."}, status=status.HTTP_400_BAD_REQUEST)
