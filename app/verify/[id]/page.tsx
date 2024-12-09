"use client";

import React, { useEffect, useState } from "react";
import { SearchParams } from "nuqs/parsers";
import { verifyProduct } from "@/data-handlers/verify-qr";
import ProductCard from "./_components/product-card";
import { ProductVerification } from "@/constants/data";

type pageProps = {
  params: { id: string };
  searchParams: SearchParams;
};

export default function Verify({ params, searchParams }: pageProps) {
  const [productData, setProductData] = useState<ProductVerification>();

  useEffect(() => {
    verifyProduct(params.id)
      .then((res) => {
        console.log(res, "RESPONSE >>>>>>>>>>>>>>>>>>>>");
        setProductData(res);
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
