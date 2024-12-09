// process.env.NODE_TLS_REJECT_UNAUTHORIZED = "0";

export const verifyProduct = async (id: string) => {
  try {
    const url = `${process.env.NEXT_PUBLIC_API_URL}isvalid/${id}`;
    console.log(`Fetching URL: ${url}`);

    const data = await fetch(url, {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
        Accept: "application/json",
        // "Origin": "http://localhost:3001", // Add this only if required for CORS
      },
    });

    if (!data.ok) {
      console.error(`HTTP error! status: ${data.status}`);
      throw new Error(`HTTP error! status: ${data.status}`);
    }

    const res = await data.json();
    return res.data;
  } catch (error) {
    console.error(`Failed to verify product ${id}:`, error);
    throw new Error("Failed to verify product. Please try again later.");
  }
};

export const markOwnership = async (id: string) => {
  try {
    const url = `${process.env.NEXT_PUBLIC_API_URL}isvalid/${id}`;
    console.log(`Fetching URL: ${url}`);

    const data = await fetch(url, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Accept: "application/json",
        // "Origin": "http://localhost:3001", // Add this only if required for CORS
      },
      body: JSON.stringify({
        is_validated: true,
      }),
    });

    if (!data.ok) {
      console.error(`HTTP error! status: ${data.status}`);
      throw new Error(`HTTP error! status: ${data.status}`);
    }

    const res = await data.json();
    return res.data;
  } catch (error) {
    console.error(`Failed to verify product ${id}:`, error);
    throw new Error("Failed to verify product. Please try again later.");
  }
};
