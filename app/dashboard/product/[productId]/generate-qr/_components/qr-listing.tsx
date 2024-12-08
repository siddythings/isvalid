import { Product } from '@/constants/data';
import { fakeProducts } from '@/constants/mock-api';
import { DataTable as ProductTable } from '@/components/ui/table/data-table';
import { columns } from './qr-tables/columns';

type ProductListingPage = {};

export default async function ProductListingPage({}: ProductListingPage) {
  // Showcasing the use of search params cache in nested RSCs

  const filters = {};

  const data = await fakeProducts.getProducts(filters);
  const totalProducts = data.total_products;
  const products: Product[] = data.products;

  return (
    <ProductTable
      columns={columns}
      data={products}
      totalItems={totalProducts}
    />
  );
}
