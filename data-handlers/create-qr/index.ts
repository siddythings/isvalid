export const createQR = async (
  productId: string,
  serialNo: string,
  batchNo?: string
) => {
  const payload = {
    product_id: productId,
    qr_details: {
      serial_no: serialNo,
      batch_no: batchNo || "",
    },
  };
  const data = await fetch(`${process.env.NEXT_PUBLIC_API_URL}create-qr`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(payload),
  });
  const res = await data.json();
  return res.data;
};
