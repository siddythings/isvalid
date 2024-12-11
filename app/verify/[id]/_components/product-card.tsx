import React from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { markOwnership } from "@/data-handlers/verify-qr";
import { useParams } from "next/navigation";
import { toast } from "sonner";
import { ProductVerification } from "@/constants/data";

interface Props {
  productData: ProductVerification;
}

const ProductCard = ({ productData }: Props) => {
  const params = useParams();
  const id = params.id as string;

  const clickHandler = () => {
    markOwnership(id)
      .then((res) => {
        toast.success("Ownership marked successfully");
      })
      .catch((err) => {
        toast.error(`${err.message}`);
      });
  };

  return (
    <div className="flex flex-col items-center">
      <div className="w-[350px] border border-gray-700 rounded-lg shadow-lg shadow-gray-900/50 hover:shadow-gray-800/50 transition-shadow my-6 mx-auto ">
        <Card>
          <CardHeader>
            <CardTitle>{productData?.product_details?.name}</CardTitle>
          </CardHeader>
          <CardContent>
            <img
              src={productData?.product_details?.image}
              alt={productData?.product_details?.name}
              style={{
                height: "auto",
                width: "100%",
              }}
            />
          </CardContent>
          <CardContent>
            <p>Price: {productData?.product_details?.price}</p>
            <br />
            <p>Description: {productData?.product_details?.description}</p>
          </CardContent>

          <CardContent>
            {!productData?.is_validated ? (
              <Button
                style={{ height: "50px", width: "100%" }}
                onClick={() => {
                  clickHandler();
                }}
              >
                Mark your ownership to prevent anyone else from being scammed.
              </Button>
            ) : (
              <div className='bg-red-600 p-3 rounded-lg'>
                <p>This product's has already been marked. May be it not original</p>
              </div>
            )}
          </CardContent>

        </Card>
      </div>
    </div>
  );
};

export default ProductCard;
