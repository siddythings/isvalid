import { Product } from '@/constants/data';
import { searchParamsCache } from '@/lib/searchparams';
import { DataTable as ProductTable } from '@/components/ui/table/data-table';
import { columns } from './product-tables/columns';
import {getProducts} from "@/data-handlers/product-data/get-products";

type ProductListingPage = {};

export default async function ProductListingPage({}: ProductListingPage) {
  // Showcasing the use of search params cache in nested RSCs
  const page = searchParamsCache.get('page');
  const search = searchParamsCache.get('q');
  const pageLimit = searchParamsCache.get('limit');
  const categories = searchParamsCache.get('categories');

  const filters = {
    page,
    limit: pageLimit,
    ...(search && { search }),
    ...(categories && { categories: categories })
  };
  const data = await getProducts();
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
