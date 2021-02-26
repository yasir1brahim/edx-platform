#!/usr/bin/python
# -*- coding: utf-8 -*-
from rest_framework.views import exception_handler
from django.http import JsonResponse
import logging
import json
import re

def is_json(myjson):
  try:
    json_object = json.loads(myjson)
  except ValueError as e:
    return False
  return True


def get_response(
    message='',
    result={},
    status=False,
    status_code=200
    ):
    return {
        'message': message,
        'result': result,
        'status': status,
        'status_code': status_code       
    }


def get_error_message(error_dict):
    field = next(iter(error_dict))
    response = error_dict[next(iter(error_dict))]
    if isinstance(response, dict):
        response = get_error_message(response)
    elif isinstance(response, list):
        response_message = response[0]
        if isinstance(response_message, dict):
            response = get_error_message(response_message)
        else:
            response = response[0]
    return response


def handle_exception(exc, context):
    error_response = exception_handler(exc, context)
    if error_response is not None:
        error = error_response.data

        if isinstance(error, list) and error:
            if isinstance(error[0], dict):
                error_response.data = \
                    get_response(message=get_error_message(error),
                                 status_code=error_response.status_code)
            elif isinstance(error[0], str):

                error_response.data = get_response(message=error[0],
                        status_code=error_response.status_code)

        if isinstance(error, dict):
            error_response.data = \
                get_response(message=get_error_message(error),
                             status_code=error_response.status_code)
    return error_response


class ExceptionMiddleware(object):

    def __init__(self,get_response):
        self.get_response = get_response

    def __call__(self, request):
       
        response = self.get_response(request)
        if not re.match(r'[\s\S]*\/v2', request.path):
            return response
       
        response_message = response.content.decode("utf-8") if response.content else ""
        if response.status_code == 500:
            response = \
                get_response(message='Internal server error, please try again later'
                             , status_code=response.status_code)
            return JsonResponse(response, status=response['status_code'
                                ])

        if response.status_code == 404:
            if 'Page not found' in str(response.content):
                response = \
                    get_response(message='Page not found, invalid url',
                             status_code=response.status_code)
            else:
                response = \
                    get_response(message=str(response.content.decode("utf-8")),
                             status_code=response.status_code)

            return JsonResponse(response, status=response['status_code'])
        elif response.status_code == 200:
            response_dict = json.loads(response.content.decode('utf-8')) if response.content else {}
            if not 'pagination' in response_dict.keys():
                response_dict['pagination']= None
            if not 'results' in response_dict.keys():
                response_dict['results'] = None
            response = \
                get_response(message='',status=True,
                             status_code=response.status_code,result=response_dict)
            return JsonResponse(response, status=response['status_code'])
        elif response.status_code == 403:
            response = \
                get_response(message=response_message,
                             status_code=response.status_code)
            return JsonResponse(response, status=response['status_code'])

        elif response.status_code == 409:
            remove_String = ['{', '}', '[', ']', '\n', '"', '           user_message: ', '      ']
            for r in remove_String:
                response_message = response_message.replace(r, '')
                response = get_response(message=response_message,status_code=409)
            return JsonResponse(response, status=response['status_code'])

        elif response.status_code == 400:
            response_dict = {}
            if is_json(response.content.decode('utf-8')):
                response_dict = json.loads(response.content.decode('utf-8')) if response.content else {}
            msg_json = response_message
            if response_dict and 'developer_message' in response_dict:
                msg_json = response_dict['developer_message']
                if not type(response_dict['developer_message']) == str:
                    msg_json = response_dict['developer_message']['developer_message']
            elif response_dict and 'message' in response_dict:
                msg_json = response_dict['message']
                if not type(response_dict['message']) == str:
                    msg_json = response_dict['message']['message']
            elif response_dict and 'field_errors' in response_dict:
                msg_json = 'Error thrown from fields'
                for key in response_dict['field_errors']:
                    msg_json = msg_json +', '+ key

                if 'date_of_birth' in response_dict['field_errors']:
                    dob_error = response_dict['field_errors']['date_of_birth']['developer_message']
                    if dob_error:
                        if "Age can't be less than 18." in dob_error:
                            msg_json = "Age can't be less than 18."
                else:
                    msg_json = msg_json + ': Please select valid values for the fields.'

                #msg_json = msg_json + ': Please select valid values for the fields.'
                #if not type(response_dict['field_errors']) == str:
                #    msg_json = response_dict['field_errors']['developer_message']

            response = \
                get_response(message=msg_json,
                             status_code=response.status_code)
            return JsonResponse(response, status=response['status_code'
                                ])
        elif response.status_code == 401:
            response_dict = json.loads(response.content.decode('utf-8')) if response.content else {}
            msg_json = response_message
            if response_dict and 'developer_message' in response_dict:
                msg_json = response_dict['developer_message']
                if not type(response_dict['developer_message']) == str:
                    msg_json = response_dict['developer_message']['developer_message']
            elif response_dict and 'message' in response_dict:
                msg_json = response_dict['message']
                if not type(response_dict['message']) == str:
                    msg_json = response_dict['message']['message']

            response = \
                get_response(message=msg_json,
                             status_code=response.status_code)
            return JsonResponse(response, status=response['status_code'
                                ])
        elif response.status_code == 409:
            response_dict = json.loads(response.content.decode('utf-8')) if response.content else {}
            msg_json = response_message
            if response_dict and 'developer_message' in response_dict:
                msg_json = response_dict['developer_message']
                if not type(response_dict['developer_message']) == str:
                    msg_json = response_dict['developer_message']['developer_message']
            elif response_dict and 'message' in response_dict:
                msg_json = response_dict['message']
                if not type(response_dict['message']) == str:
                    msg_json = response_dict['message']['message']

            response = \
                get_response(message=msg_json,
                             status_code=response.status_code)
            return JsonResponse(response, status=response['status_code'
                                ])


        else:
            pass
        return response

