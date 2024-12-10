import { Product } from "@/constants/data";
import { DataTable as ProductTable } from "@/components/ui/table/data-table";
import { columns } from "./qr-tables/columns";

type ProductListingPage = {
  productData: any;
};

export default async function ProductListingPage({
  productData,
}: ProductListingPage) {
  if (!productData?.length) {
    return <>No Records</>;
  }

  const totalProducts = productData.length;
  const products: Product[] = productData;

  return (
    <ProductTable
      columns={columns}
      data={products}
      totalItems={totalProducts}
    />
  );
}
