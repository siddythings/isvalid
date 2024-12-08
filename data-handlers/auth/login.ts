export const userLogin = async (email: string, password: string) => {
  const payload = {
    email,
    password,
  };

  const data = await fetch(`${process.env.NEXT_PUBLIC_AUTH_URL}auth/user/login`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(payload),
  });
  const res = await data.json();
  return res.data;
};
