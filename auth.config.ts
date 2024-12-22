import { NextAuthConfig } from 'next-auth';
import CredentialsProvider from 'next-auth/providers/credentials';
import GithubProvider from 'next-auth/providers/github';

const authConfig: NextAuthConfig = {
  providers: [
    GithubProvider({
      clientId: process.env.GITHUB_ID ?? '',
      clientSecret: process.env.GITHUB_SECRET ?? '',
    }),
    CredentialsProvider({
      name: 'Credentials',
      credentials: {
        name: { label: 'Name', type: 'text' },
        email: { label: 'Email', type: 'email' },
        password: { label: 'Password', type: 'password' },
      },
      async authorize(credentials) {
        // Validate the credentials (e.g., query your database or external API)
        if (credentials) {
          const user = {
            id: '1', // Replace with actual user ID
            name: credentials.name as string,
            email: credentials.email as string,
            emailVerified: null, // Include this property
          };

          // Validate user data (e.g., check password, etc.)
          if (user.name && user.email) {
            return user; // Must return an object matching the AdapterUser type
          }
        }

        // Return null if user authentication fails
        return null;
      },
    }),
  ],
  pages: {
    signIn: '/', // Custom sign-in page
  },
  secret: process.env.NEXTAUTH_SECRET,
  session: {
    strategy: 'jwt',
  },
  callbacks: {
    async jwt({ token, user }) {
      if (user) {
        token.id = user.id;
        token.name = user.name;
        token.email = user.email;
      }
      return token;
    },
    async session({ session, token }) {
      if (token) {
        // @ts-ignore
        session.user = {
          id: token.id as string,
          name: token.name as string,
          email: token.email as string,
        };
      }
      return session;
    },
  },
  debug: true, // Enable detailed logging
};

export default authConfig;
