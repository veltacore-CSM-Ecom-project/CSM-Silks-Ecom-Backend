from __future__ import annotations

from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView

from catalog.models import Product
from catalog.selectors import public_products
from catalog.serializers import ProductListSerializer

from .models import TryOnSession
from .serializers import TryOnSerializer, VoiceSearchSerializer


class TryOnView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def post(self, request):
        serializer = TryOnSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        product = None
        if serializer.validated_data.get("product_id"):
            product = get_object_or_404(Product, id=serializer.validated_data["product_id"])
        drape_style = serializer.validated_data.get("drape_style", "traditional")
        body_type = serializer.validated_data.get("body_type", "regular")
        skin_tone = serializer.validated_data.get("skin_tone", "medium")
        product_name = product.name if product else "this CSM silk weave"
        result = {
            "draping_tip": f"For {drape_style} on a {body_type} frame, keep pleats crisp and let the pallu fall cleanly for {product_name}.",
            "colour_analysis": f"Warm gold and jewel tones complement {skin_tone} skin beautifully for festive wear.",
            "blouse_suggestion": "Pair with antique gold tissue or contrast zari blouse to highlight the weave.",
            "jewellery_pairing": "Temple jhumkas or kundan with a single strand of pearls balances the silk drape.",
            "footwear": "Block heels or embellished flats keep the look comfortable through long ceremonies.",
            "confidence_score": 92 if product else 88,
            "ai_verdict": f"{product_name} is a strong occasion-ready choice from the CSM Silks collection.",
            "alternative_colours": ["Gold", "Maroon", "Bottle green"],
        }
        session = TryOnSession.objects.create(
            user=request.user if request.user.is_authenticated else None,
            product=product,
            skin_tone=serializer.validated_data.get("skin_tone", "medium"),
            body_type=serializer.validated_data.get("body_type", "regular"),
            drape_style=serializer.validated_data.get("drape_style", "traditional"),
            occasion=serializer.validated_data.get("occasion", ""),
            ai_result=result,
            confidence_score=result["confidence_score"],
        )
        return Response({"session_id": session.id, **result})


class VoiceSearchView(APIView):
    def post(self, request):
        serializer = VoiceSearchSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        transcript = serializer.validated_data["transcript"]
        return Response({"intent": "search", "search_query": transcript, "response_text": f"Searching CSM Silks for {transcript}", "filters": {}})


class RecommendView(APIView):
    def get(self, request):
        products = public_products({"featured": "true"})[:6]
        return Response({"items": ProductListSerializer(products, many=True).data})

    def post(self, request):
        return self.get(request)
