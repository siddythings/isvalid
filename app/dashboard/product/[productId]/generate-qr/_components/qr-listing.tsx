import { Product } from '@/constants/data';
import { DataTable as ProductTable } from '@/components/ui/table/data-table';
import { columns } from './qr-tables/columns';
import { getProductQRByID } from '@/data-handlers/product-data/get-products';

type ProductListingPage = {
  productID: string
};

export default async function ProductListingPage({productID}: ProductListingPage) {
  // Showcasing the use of search params cache in nested RSCs

  const data = await getProductQRByID(productID);
  
  if (!data?.length) {
    return <>No Records</>;
  }

  const totalProducts = data.length;
  const products: Product[] = data;

  return (
    <ProductTable
      columns={columns}
      data={products}
      totalItems={totalProducts}
    />
  );
}
