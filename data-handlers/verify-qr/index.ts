process.env.NODE_TLS_REJECT_UNAUTHORIZED = "0";

export const verifyProduct = async (id: string) => {
  try {
    const data = await fetch(`https://api.lnkr.store/api/v1/isvalid/675575c0bd7cd545a3d2c723`, {
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
    console.error(`Failed to verify product ${id}:`, error);
    throw new Error('Failed to verify product. Please try again later.');
  }
};
