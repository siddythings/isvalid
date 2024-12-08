"use client";
import { Product } from "@/constants/data";
import { ColumnDef } from "@tanstack/react-table";
import Image from "next/image";
import { CellAction } from "./cell-action";
import {CellQRAction} from './cell-qr-action'

export const columns: ColumnDef<Product>[] = [
  {
    accessorKey: "product_details.image",
    header: "IMAGE",
    cell: ({ row }) => {
      const productDetails = row.original.product_details; // Access the nested object
      const image = productDetails?.image || ""; // Get the image URL safely
  
      return (
        <div className="relative aspect-square w-16 h-16">
          {image ? (
            <Image
              src={image}
              alt={productDetails?.name || "Product Image"}
              fill
              className="rounded-lg object-cover"
            />
          ) : (
            <div className="bg-gray-200 rounded-lg flex items-center justify-center">
              <span>No Image</span>
            </div>
          )}
        </div>
      );
    },
  },
  {
    accessorKey: "product_details.name",
    header: "NAME",
  },
  {
    accessorKey: "product_details.price",
    header: "PRICE",
  },
  {
    accessorKey: "product_details.description",
    header: "DESCRIPTION",
  },

  {
    accessorKey: "Actions",
    cell: ({ row }) => <CellAction data={row.original} />,
  },

  {
    id: "actions",
    cell: ({ row }) => <CellQRAction data={row.original} />,
  },
];
