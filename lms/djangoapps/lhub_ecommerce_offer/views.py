from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

import logging

# Create your views here.

class Ecommerce_Offer(APIView):

    def post(self, request):
        ecommerce_data = request.data
        logging.info("=======**********************==========")
        logging.info(ecommerce_data)
        
        associated_ecommerce_offer_id = ecommerce_data['associated_ecommerce_offer_id']
        start_datetime = ecommerce_data['start_datetime']
        end_datetime = ecommerce_data['end_datetime']
        priority = ecommerce_data['priority']
        incentive_type = ecommerce_data['incentive_type']
        incentive_value = ecommerce_data['incentive_value']
        condition_type = ecommerce_data['condition_type']
        condition_value = ecommerce_data['condition_value']
        is_exclusive = ecommerce_data['is_exclusive']
        courses_sku = ecommerce_data['courses_sku']

        


        
        return Response({'status': 'Succes'}, status=status.HTTP_200_OK)