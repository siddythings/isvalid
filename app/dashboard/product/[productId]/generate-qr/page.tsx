import FormCardSkeleton from "@/components/form-card-skeleton";
import PageContainer from "@/components/layout/page-container";
import { Suspense } from "react";
import QrListing from "./_components/qr-listing";
import QRForm from "./_components/qr-form";
import { getProductQRByID } from "@/data-handlers/product-data/get-products";

export const metadata = {
  title: "Dashboard : QR Listing",
};

type PageProps = { params: { productId: string } };

export default async function Page({ params }: PageProps) {
  const data = await getProductQRByID(params?.productId);

  return (
    <PageContainer scrollable>
      <div className="flex-1 space-y-4">
        <Suspense>
          <QRForm />
        </Suspense>
        <Suspense fallback={<FormCardSkeleton />}>
          <QrListing productData={data} />
        </Suspense>
      </div>
    </PageContainer>
  );
}
