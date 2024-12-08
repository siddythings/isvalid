import { fakeProducts, Product } from '@/constants/mock-api';
import { notFound } from 'next/navigation';
import ProductForm from './product-form';
import { getProductQRByID } from '@/data-handlers/product-data/get-products';

type TProductViewPageProps = {
  productId: string;
};

export default async function ProductViewPage({
  productId
}: TProductViewPageProps) {
  let product = null;
  let pageTitle = 'Create New Product';

  if (productId !== 'new') {
    const data = await getProductQRByID(productId);
    product = data.product as Product;
    if (!product) {
      notFound();
    }
    pageTitle = `Edit Product`;
  }

  return <ProductForm initialData={product} pageTitle={pageTitle} />;
}
