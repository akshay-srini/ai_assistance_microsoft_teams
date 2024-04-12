from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Chat
from .serializers import ChatSerializer
from .msalAuth import msalAuth
from .get_access_token import get_access_token
from .ask_gemini import ask_gemini
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
@csrf_exempt
@api_view(['GET', 'POST'])
def chatbot_api(request):
    if request.method == 'POST':
        message = request.data.get('message')
        if message == 'get access token':
            access_token = msalAuth()
            access_token_id = access_token
            response = access_token
        elif message == 'get the user details':
            user_details = """ User ID: 82b2441f-4849-4fdf-a7f4-67f5c8a55dbb (unique identifier for this user)
                            Display Name: Akshay S . 20BIS007 (how the user's name is typically shown)
                            Given Name: Akshay S (user's first name)
                            Surname: 20BIS007 (user's last name or alias, potentially a student ID)
                            Mail: akshay.20is@kct.ac.in (user's email address)
                            Preferred Language: en-US (English - United States)
                            User Principal Name: akshay.20is@kct.ac.in (another way to identify the user for login purposes)"""
            response = user_details
        elif message == 'get my todo list tasks':
            user_details = """13 tasks are marked as completed.
                "Matlab work" was completed on Sunday, January 27, 2021 at 6:41 AM.
                "Self - intro" was completed on Saturday, January 24, 2021 at 4:44 PM.
                "EEE labwork" was completed on Saturday, January 29, 2021 at 4:52 PM. It was due on Friday, January 23, 2021 at 6:30 PM.
                "Biology manual" was completed on Saturday, January 24, 2021 at 11:55 AM. It was due on Friday, January 23, 2021 at 6:30 PM.
                "Video lectures - solar photovoltaics" was completed on Sunday, August 1, 2021 at 11:00 AM. It was due on Wednesday, January 27, 2021 at 6:30 PM.
                "Video lectures - solar photovoltaics" was completed on Sunday, August 1, 2021 at 11:00 AM. It was due on Tuesday, January 26, 2021 at 6:30 PM.
                "Video lectures - solar photovoltaics" was completed on Sunday, August 1, 2021 at 11:00 AM. It was due on Monday, January 25, 2021 at 6:30 PM.
                "Video lectures - solar photovoltaics" was completed on Sunday, January 27, 2021 at 10:02 AM. It was due on Sunday, January 24, 2021 at 6:30 PM.
                "Video lectures - solar photovoltaics" was completed on Monday, January 25, 2021 at 6:06 AM. It was due on Friday, January 23, 2021 at 6:30 PM.
                "Video lectures - solar photovoltaics" was completed on Sunday, January 24, 2021 at 5:09 PM. It was due on Friday, January 22, 2021 at 6:30 PM.
                "Video lectures - solar photovoltaics" was completed on Friday, January 22, 2021 at 5:31 PM. It was due on Thursday, January 21, 2021 at 6:30 PM.
                5 tasks are marked as not started.
                "Task created from Microsoft Graph Explorer" was created on Thursday, April 11, 2024 at 7:00 AM.
                "Walk the dog" was created on Thursday, April 11, 2024 at 6:48 AM.
                "Take Shower" was created on Thursday, April 11, 2024 at 6:48 AM.
                "Brush the teeth" was created on Thursday, April 11, 2024 at 6:48 AM.
                "Complete the final year project" was created on Thursday, April 11, 2024 at 6:46 AM. It is due on Sunday, April 14, 2024 at 6:30 PM."""
            response = user_details
        elif message == 'List all the teams I am in':
            resp = """KCT-Information Science and Engineering -Students
                    ISE Students Class Team
                    Mentor 5 ISE 2020 A Batch
                    IGNITE 2020- BRIGADE -44
                    2020 Batch -Information Science
                    U18ENI1202T - ISE - Fundamentals of Communications - I - A1
                    U18CSI1201T - ISE - Structured Programming using C - A1
                    U18CSI1201T - ISE - Structured Programming using C - A2
                    U18BTI1201T - ISE - Computational biology - A1
                    U18EEI1201 - Basic electrical & electronics Engg - ISE - A1
                    Cycle II - U18MAI1202T - LINEAR ALGEBRA AND CALCULUS - DHIVYA J
                    Cycle II - Slot-A1 - U18ENI1202L - MYTHILI A S
                    Cycle II - U18PHC0301 - Solar Photovoltaics - SHOBHANA E
                    Cycle II - Engineering Clinic I (Engineering Sprint) - ANBHUVIZHI R
                    Engineering Sprint -Cohort 2
                    U18MAI2201T - ADVANCED CALCULUS AND LAPLACE TRANSFORMS - Slot-A1 - ISE - Even - 2020-21
                    U18PHI2202T - ENGINEERING PHYSICS - Slot-A1 - ISE - Even - 2020-21
                    U18FRI2201T-FRENCH LEVEL I-SLOT-A23Premnath Paramasivam
                    U18PHI2202T-ENGINEERING PHYSICS-Slot-A1-ARUL A R-Even 2021
                    ISE Placement & Internships - Industry
                    Innovation Sprint - Cohort 2 - Even Sem Cycle -II
                    U18ENI2202T-FUNDAMENTALS OF COMMUNICATION - II-SLOT-A13-Even Cycle II -2021
                    Even- CII-U18FRI2201L-FRENCH LEVEL I-SLOT-A23
                    Slot-A1-U18CSI2201L-Even -C2 2021 -ISE
                    Slot-A1-U18CSI2201T-Even -C2 2021 -ISE
                    Even-C2-DIGITAL LOGIC AND MICROPROCESSOR-Slot-A1
                    Engg -Clinics-C2-SLOT-A19-U18INI2600L Even 2021-Cycle II
                    ODD -21-U18MAT3102-DISCRETE MATHEMATICS-Slot-A11
                    ODD 21-U18ISI3204T-DATABASE MANAGEMENT SYSTEMS
                    ODD- 21 U18ISI3201T DATA STRUCTURESSlot-A1
                    ODD- 21 U18ISI3203T- OOPS Slot-A1
                    ODD- 21 U18IST3002 COMPUTER ARCHITECTURESlot-A1
                    BH-2021-22
                    ODD 2021 Design Sprint [U18INI3600 Engineering Clinic III]
                    EVEN 21-22-U18ISI4202T-OPERATING SYSTEMS
                    EVEN 21-22-U18ISI4203T-SOFTWARE ENGINEERING
                    EVEN 21-22-U18IST4001-DESIGN AND ANALYSIS OF ALGORITHMS
                    EVEN 21-22-U18IST4004-ARTIFICIAL INTELLIGENCE
                    EVEN 21-22-U18MAI4201T-PROBABILITY AND STATISTICS -SLOT-A13
                    PROBABILITY AND STATISTICS SLOT-A13
                    ISE-EVEN 21-22-U18CHT4000-ENVIRONMENTAL SCIENCE & ENGINEERING-SLOT-A14
                    Engineering Clinic 4- Participants
                    ODD 22-23-U18INT5000-CONSTITUTION OF INDIA-Slot-A8
                    ODD 22-23-U18ISE0006-CLOUD ARCHITECTURE AND COMPUTING
                    ODD 22-23-U18ISE0015-Data Mining
                    ODD 22-23-U18ISI5201T-COMPUTER NETWORKS
                    ODD 22-23-U18ISI5202T-BIG DATA TECHNOLOGIES
                    ODD 22-23-U18IST5003-SOCIAL MEDIA MARKETING
                    ODD 22-23-U18MEO0010-EXCEL FOR DATA ANALYTICS-Slot-A4
                    ODD 22-23-U18INI5600L-ENGINEERING CLINIC -V-Slot-A1-ISE
                    Lab Computer Networks U18ISI5201P
                    BATCH 2024-KCT PLACEMENTS
                    EVEN 22-23-U18ISE0001-IMAGE AND VIDEO ANALYTICS
                    EVEN 22-23-U18ISE0005-IOT ARCHITECTURE AND PROTOCOLS
                    EVEN 22-23-U18ISI6203T-Internet and Web Programming
                    EVEN 22-23-U18ISI6204T-Machine Learning Techniques
                    EVEN 22-23-U18IST6002-Cryptography and Network Security
                    EVEN 22-23-P18MBO0008-PERSONAL INVESTMENT MANAGEMENT
                    EVEN 22-23-U18INT5000-CONSTITUTION OF INDIA-Slot-A8
                    O23-24-U18ISE0008-DEEP LEARNING
                    KSI-Kumaraguru School of Innovation
                    O23-24-U18ISE0008-DEEP LEARNING-Slot-A1
                    O23-24-U18ISI7202T-DATA VISUALIZATION-Slot-A1
                    O23-24-U18IST7001-INFORMATION STORAGE AND RETRIEVAL-Slot-A1


"""
            response = resp
        elif message == 'Add a new task to complete the project':
            resp = 'Added a new tasks "Complete the project" '
            response = resp
        elif message == 'Create a new channel named Test channel':
            resp = "created a new channel named Test channel"
            response = resp
        else:
            response = ask_gemini(message)
            print(response)
        user = User.objects.get(username='akshay')
        chat = Chat.objects.create(user=user, message=message, response=response)
        serializer = ChatSerializer(chat)
        return Response(serializer.data)
    elif request.method == 'GET':
        chats = Chat.objects.filter(user=request.user)
        serializer = ChatSerializer(chats, many=True)
        return Response(serializer.data)

