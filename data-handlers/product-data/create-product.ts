import { Product } from "@/constants/data";
import { v4 as uuidv4 } from 'uuid';

export const getImageURL = async (file: File) => {
  const preSignedUrl = await fetch(`${process.env.NEXT_PUBLIC_API_URL}upload`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ file_name: `${uuidv4()}.${file?.type.split('/')[1]}` }),
  });

  const data = await preSignedUrl.json();
  
  const uploadUrl = data?.data.presigned_url;
  const response = await fetch(uploadUrl, {
    method: "PUT",
    headers: {
      "Content-Type": file.type,
    },
    body: file,
  });
  const finalURL = data.data.url;
  console.log(response);

  return finalURL;
};

export const createProduct = async (product: any) => {
  const imageURL = await getImageURL(product.image[0]);
  const payload = {
    product_details: {
      name: product.name,
      price: product.price,
      description: product.description,
      image: imageURL,
    },
  };

  const data = await fetch(`${process.env.NEXT_PUBLIC_API_URL}product`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(payload),
  });
  return data.json();
};
