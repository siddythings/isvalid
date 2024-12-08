"use client";
import { Product } from "@/constants/data";
import { ColumnDef } from "@tanstack/react-table";
import Image from "next/image";
import QRCode from "react-qr-code";
// import { CellAction } from './cell-action';

export const columns: ColumnDef<Product>[] = [
  {
    accessorKey: "photo_url",
    header: "QR-IMAGE",
    cell: ({ row }) => {
      return (
        <div className="relative w-max">
          <QRCode
            size={100}
            style={{ height: "auto", maxWidth: "80px", width: "80px" }}
            value={"https://www.youtube.com/watch?v=NkwFxeHARqc"}
            viewBox={`0 0 256 256`}
          />
        </div>
      );
    },
  },
  {
    accessorKey: "qr-id",
    header: "QR-ID",
  },
  {
    accessorKey: "qr-link",
    header: "QR LINK",
  },
  {
    accessorKey: "qr-download",
    header: "DOWNLOAD",
  },
  //   {
  //     accessorKey: 'description',
  //     header: 'DESCRIPTION'
  //   },

  //   {
  //     id: 'actions',
  //     cell: ({ row }) => <CellAction data={row.original} />
  //   }
];
