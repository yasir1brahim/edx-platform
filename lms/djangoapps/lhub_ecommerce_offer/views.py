from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Offer
import datetime
from openedx.core.djangoapps.content.course_overviews.models import CourseOverview
import logging

# Create your views here.

class Ecommerce_Offer(APIView):

    def post(self, request):
        ecommerce_data = request.data

        # If Offer already exists
        # update it
        if Offer.objects.filter(associated_ecommerce_offer_id = ecommerce_data['associated_ecommerce_offer_id']).exists():
            ecommerce_offer = Offer.objects.filter(associated_ecommerce_offer_id = ecommerce_data['associated_ecommerce_offer_id'])
            # update_ecommerce_offer = Offer.objects.get(associated_ecommerce_offer_id = ecommerce_data['associated_ecommerce_offer_id'])
            ecommerce_offer.update(
                associated_ecommerce_offer_id = ecommerce_data['associated_ecommerce_offer_id'],
                # start_datetime = ecommerce_data['start_datetime'],
                # end_datetime = ecommerce_data['end_datetime'],
                priority = ecommerce_data['priority'],
                incentive_type = ecommerce_data['incentive_type'],
                incentive_value = ecommerce_data['incentive_value'],
                condition_type = ecommerce_data['condition_type'],
                condition_value = ecommerce_data['condition_value'],
                is_exclusive = ecommerce_data['is_exclusive'],

                start_datetime = datetime.datetime.now(),
                end_datetime = datetime.datetime.now()
            )

            for course in ecommerce_offer[0].course.all():
                # condition 01: course is present in Offer courses
                # and also in the api courses
                if str(course.id) in ecommerce_data['courses_id']:
                    # do nothing
                    pass
                # condition 02: course is present in offer courses
                # but not in the api courses
                elif str(course.id) not in ecommerce_data['courses_id']:
                    # remove the course from Offer courses
                    course.delete()
 
            # condition 03: course is not present in offer courses
            # but present in the api courses
            for course in ecommerce_data['courses_id']:
                if course not in str(ecommerce_offer[0].course.all()):
                    # add course in the Offer courses
                    ecommerce_offer[0].course.add(CourseOverview.get_from_id(course))    

        else: 
            ecommerce_offer = Offer(
                associated_ecommerce_offer_id = ecommerce_data['associated_ecommerce_offer_id'],
                # start_datetime = ecommerce_data['start_datetime'],
                # end_datetime = ecommerce_data['end_datetime'],
                priority = ecommerce_data['priority'],
                incentive_type = ecommerce_data['incentive_type'],
                incentive_value = ecommerce_data['incentive_value'],
                condition_type = ecommerce_data['condition_type'],
                condition_value = ecommerce_data['condition_value'],
                is_exclusive = ecommerce_data['is_exclusive'],

                start_datetime = datetime.datetime.now(),
                end_datetime = datetime.datetime.now()
            )   

            ecommerce_offer.save()  

            for course_id in ecommerce_data['courses_id']:
                ecommerce_offer.course.add(CourseOverview.get_from_id(course_id))

        
        return Response({'status': 'Succes'}, status=status.HTTP_200_OK)