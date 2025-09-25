from core.settings import plaid_client # CORRECT: Import the variable directly
from django.contrib.auth.models import User

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

# Imports for Plaid
from plaid.model.link_token_create_request import LinkTokenCreateRequest
from plaid.model.link_token_create_request_user import LinkTokenCreateRequestUser
from plaid.model.products import Products
from plaid.model.country_code import CountryCode
from plaid.exceptions import ApiException


class CreateLinkTokenView(APIView):
    """
    Handles the creation of a Plaid link_token.

    A link_token is a temporary, one-time-use token that is used to
    initialize the Plaid Link frontend experience.
    """
    # For development, we can allow any user to access this endpoint
    # In production, you'll want to lock this down to authenticated users
    authentication_classes = []
    permission_classes = []

    def post(self, request, *args, **kwargs):
        try:
            # For this development example, we'll just use the first user
            # in the database (your superuser). In a real app, you would
            # use the currently logged-in user: request.user
            user = User.objects.first()
            if not user:
                return Response(
                    {"error": "No user found in the database. Please create a superuser."},
                    status=status.HTTP_404_NOT_FOUND
                )

            # Create the Plaid LinkTokenCreateRequest object
            plaid_request = LinkTokenCreateRequest(
                user=LinkTokenCreateRequestUser(
                    client_user_id=str(user.id) # A unique ID for the user
                ),
                client_name="Personal Finance App",
                products=[Products("auth"), Products("transactions")],
                country_codes=[CountryCode('US')],
                language='en',
            )

            # Make the API call to Plaid to create the link_token
            response = plaid_client.link_token_create(plaid_request)

            # Return the link_token to the frontend
            return Response({'link_token': response['link_token']})

        except ApiException as e:
            # Handle Plaid API errors
            error_details = e.body
            return Response(
                {"error": "Could not create link token.", "details": error_details},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        except Exception as e:
            # Handle other potential errors
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

