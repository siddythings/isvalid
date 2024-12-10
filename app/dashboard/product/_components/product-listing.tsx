import { Product } from '@/constants/data';
import { DataTable as ProductTable } from '@/components/ui/table/data-table';
import { columns } from './product-tables/columns';


type ProductListingPageProps = {
  productData: Product[];
};

export default async function ProductListingPage({ productData }: ProductListingPageProps) {
  const totalProducts = productData && productData.length;
  const products: Product[] = productData;  
  return (
    <ProductTable
      columns={columns}
      data={products}
      totalItems={totalProducts}
    />
  );
}
