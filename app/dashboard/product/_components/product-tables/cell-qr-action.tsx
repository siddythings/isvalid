"use client";
import { useRouter } from "next/navigation";
import { Button } from "@/components/ui/button";

import { Product } from "@/constants/data";

interface CellActionProps {
  data: Product;
}

export const CellQRAction: React.FC<CellActionProps> = ({ data }) => {
  const router = useRouter();
  return (
    <>
      <Button onClick={() => router.push(`/dashboard/product/${data?.id}/generate-qr`)}>Generate QR</Button>
    </>
  );
};
