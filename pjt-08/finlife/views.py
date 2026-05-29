from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import get_object_or_404

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .serializers import (
    DepositProductsSerializer,
    DepositOptionsSerializer,
)

import requests

from .models import DepositProducts, DepositOptions


# F801
@api_view(['GET'])
def save_deposit_products(request):

    api_key = settings.FINLIFE_API_KEY

    url = "http://finlife.fss.or.kr/finlifeapi/depositProductsSearch.json"

    params = {
        'auth': api_key,
        'topFinGrpNo': '020000',
        'pageNo': 1
    }

    response = requests.get(url, params=params).json()

    base_list = response.get('result', {}).get('baseList', [])
    option_list = response.get('result', {}).get('optionList', [])

    # 상품 저장
    for product_data in base_list:

        if not DepositProducts.objects.filter(
            fin_prdt_cd=product_data.get('fin_prdt_cd')
        ).exists():

            DepositProducts.objects.create(
                fin_prdt_cd=product_data.get('fin_prdt_cd'),
                kor_co_nm=product_data.get('kor_co_nm'),
                fin_prdt_nm=product_data.get('fin_prdt_nm'),
                etc_note=product_data.get('etc_note'),
                join_deny=product_data.get('join_deny'),
                join_member=product_data.get('join_member'),
                join_way=product_data.get('join_way'),
                spcl_cnd=product_data.get('spcl_cnd')
            )

    # 옵션 저장
    for option_data in option_list:

        product = DepositProducts.objects.filter(
            fin_prdt_cd=option_data.get('fin_prdt_cd')
        ).first()

        if product:

            intr_rate = option_data.get('intr_rate')

            if intr_rate is None:
                intr_rate = -1

            intr_rate2 = option_data.get('intr_rate2')

            if intr_rate2 is None:
                intr_rate2 = -1

            # 중복 저장 방지
            if not DepositOptions.objects.filter(
                product=product,
                save_trm=option_data.get('save_trm'),
                intr_rate_type_nm=option_data.get('intr_rate_type_nm')
            ).exists():

                DepositOptions.objects.create(
                    product=product,
                    fin_prdt_cd=option_data.get('fin_prdt_cd'),
                    intr_rate_type_nm=option_data.get('intr_rate_type_nm'),
                    intr_rate=intr_rate,
                    intr_rate2=intr_rate2,
                    save_trm=option_data.get('save_trm')
                )

    return JsonResponse({"message": "okay"})


# F802 + F803
@api_view(['GET', 'POST'])
def deposit_products(request):

    # 전체 조회
    if request.method == 'GET':

        products = DepositProducts.objects.all()

        serializer = DepositProductsSerializer(
            products,
            many=True
        )

        return Response(serializer.data)

    # 상품 추가
    elif request.method == 'POST':

        serializer = DepositProductsSerializer(
            data=request.data
        )

        if serializer.is_valid():

            serializer.save()

            return Response(
                {
                    "message": "데이터 삽입 성공",
                    "data": serializer.data
                },
                status=status.HTTP_201_CREATED
            )

        return Response(
            {
                "message": "데이터 삽입 실패",
                "errors": serializer.errors
            },
            status=status.HTTP_400_BAD_REQUEST
        )


# F804
@api_view(['GET'])
def deposit_product_options(request, fin_prdt_cd):

    # 상품 조회
    product = get_object_or_404(
        DepositProducts,
        fin_prdt_cd=fin_prdt_cd
    )

    # 연결된 옵션 조회
    options = product.depositoptions_set.all()

    serializer = DepositOptionsSerializer(
        options,
        many=True
    )

    return Response(serializer.data)


# F806
@api_view(['GET'])
def top_rate(request):

    # 최고 우대금리 옵션 조회
    top_option = DepositOptions.objects.order_by(
        '-intr_rate2'
    ).first()

    # 연결된 상품
    product = top_option.product

    product_serializer = DepositProductsSerializer(product)

    option_serializer = DepositOptionsSerializer(top_option)

    return Response({
        'product': product_serializer.data,
        'option': option_serializer.data,
    })