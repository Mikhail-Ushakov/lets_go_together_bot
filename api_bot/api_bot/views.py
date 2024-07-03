from django.shortcuts import render
from rest_framework.generics import CreateAPIView
# Create your views here.
# class RegisterView(CreateAPIView):
#     """
#     Register a new user to the system
#     """

#     permission_classes = import_string_list(drfr_settings.REGISTER_PERMISSION_CLASSES)
#     serializer_class = import_string(drfr_settings.REGISTER_SERIALIZER)

#     def post(self, request, *args, **kwargs):
#         serializer = self.serializer_class(data=request.data)
#         serializer.is_valid(raise_exception=True)

#         user = serializer.save()
#         data = get_user_profile_data(user)

#         domain = get_current_domain(request)

#         # Send email activation link
#         if has_user_activate_token() or has_user_verify_code():
#             send_verify_email(user, domain)
#         else:
#             send_email_welcome(user)

#         return Response(data, status=status.HTTP_201_CREATED)