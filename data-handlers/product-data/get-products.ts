process.env.NODE_TLS_REJECT_UNAUTHORIZED = "0";

export const getProducts = async () => {
  const data = await fetch(`${process.env.NEXT_PUBLIC_API_URL}products`, {
    method: "GET",
    headers: {
      "Content-Type": "application/json",
    },
  });
  const res = await data.json();
  return res.data
};
export const getProductQRByID = async (id:string) => {
  const data = await fetch(`${process.env.NEXT_PUBLIC_API_URL}qr/${id}`, {
    method: "GET",
    headers: {
      "Content-Type": "application/json",
    },
  });
  const res = await data.json();
  return res.data
};
