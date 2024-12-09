import React from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { markOwnership } from "@/data-handlers/verify-qr";
import { useParams } from "next/navigation";
import { toast } from "sonner";

interface Props {
  productData: {
    name: string;
    price: string;
    image: string;
    description: string;
  };
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
            <CardTitle>{productData?.name}</CardTitle>
          </CardHeader>
          <CardContent>
            <img
              src={productData?.image}
              alt={productData?.name}
              style={{
                height: "auto",
                width: "100%",
              }}
            />
          </CardContent>
          <CardContent>
            <p>Price: {productData?.price}</p>
            <br />
            <p>Description: {productData?.description}</p>
          </CardContent>
        </Card>
      </div>

      <Button
        onClick={() => {
          clickHandler();
        }}
      >
        Mark Ownership
      </Button>
    </div>
  );
};

export default ProductCard;
