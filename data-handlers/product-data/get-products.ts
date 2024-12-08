process.env.NODE_TLS_REJECT_UNAUTHORIZED = "0";

export const getProducts = async () => {
  try {
    const data = await fetch(`${process.env.NEXT_PUBLIC_API_URL}products`, {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
      },
    });
    
    if (!data.ok) {
      throw new Error(`HTTP error! status: ${data.status}`);
    }
    
    const res = await data.json();
    return res.data;
  } catch (error) {
    console.error('Failed to fetch products:', error);
    throw new Error('Failed to fetch products. Please try again later.');
  }
};

export const getProductQRByID = async (id: string) => {
  try {
    const data = await fetch(`${process.env.NEXT_PUBLIC_API_URL}qr/${id}`, {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
      },
    });
    
    if (!data.ok) {
      throw new Error(`HTTP error! status: ${data.status}`);
    }
    
    const res = await data.json();
    return res.data;
  } catch (error) {
    console.error(`Failed to fetch QR for product ${id}:`, error);
    throw new Error('Failed to fetch product QR code. Please try again later.');
  }
};