"use client";

import React, { useEffect, useState } from "react";
import { SearchParams } from "nuqs/parsers";
import { verifyProduct } from "@/data-handlers/verify-qr";
import ProductCard from "./_components/product-card";

type pageProps = {
  params: { id: string };
  searchParams: SearchParams;
};

export default function Verify({ params, searchParams }: pageProps) {
  const [productData, setProductData] = useState<{
    name: string;
    price: string;
    image: string;
    description: string;
  }>();

  useEffect(() => {
    verifyProduct(params.id)
      .then((res) => {
        console.log(res, "RESPONSE >>>>>>>>>>>>>>>>>>>>");
        setProductData(res.product_details); // Store the response in state
      })
      .catch((err) => {
        console.log(err.message, "ERROR_MESSAGE >>>>>>>>>>>>>>>>>");
      });
  }, [params.id]);

  return (
    <>
      {productData && <ProductCard productData={productData} />}
    </>
  );
}
