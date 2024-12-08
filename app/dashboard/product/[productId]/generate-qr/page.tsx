import FormCardSkeleton from "@/components/form-card-skeleton";
import PageContainer from "@/components/layout/page-container";
import { Suspense } from "react";
import { fakeProducts, fakeUsers } from "@/constants/mock-api";
import { DataTable as ProductTable } from "@/components/ui/table/data-table";
import { searchParamsCache } from "@/lib/searchparams";
import { columns } from "../../../product/_components/product-tables/columns";
import { Product } from "@/constants/data";
import QrListing from "./_components/qr-listing";
import QRForm from "./_components/qr-form";

export const metadata = {
  title: "Dashboard : QR Listing",
};

type PageProps = { params: { productId: string } };

export default async function Page({ params }: PageProps) {
  return (
    <PageContainer scrollable>
      <div className="flex-1 space-y-4">
        <Suspense>
          <QRForm />
        </Suspense>
        <Suspense fallback={<FormCardSkeleton />}>
          <QrListing />
        </Suspense>
      </div>
    </PageContainer>
  );
}
