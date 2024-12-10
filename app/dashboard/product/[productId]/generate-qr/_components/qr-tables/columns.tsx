"use client";
import { Product } from "@/constants/data";
import { ColumnDef } from "@tanstack/react-table";
import QRCode from "react-qr-code";
import { Button } from "@/components/ui/button"; 

export const columns: ColumnDef<Product>[] = [
  {
    accessorKey: "url",
    header: "QR-IMAGE",
    cell: ({ row }) => {
      const url = row.original.url;
      return (
        <div className="relative w-max">
          <QRCode
            size={100}
            style={{ height: "auto", maxWidth: "80px", width: "80px" }}
            value={url}
            viewBox={`0 0 256 256`}
            data-qr-id={row.original.id}
          />
        </div>
      );
    },
  },
  {
    accessorKey: "id",
    header: "QR-ID",
  },
  {
    accessorKey: "url",
    header: "QR LINK",
    cell: ({ row }) => (
      <a href={row.original.url} target="_blank" rel="noopener noreferrer" className="text-blue-600 hover:underline">
        {row.original.url}
      </a>
    ),
  },
  {
    accessorKey: "qr-download",
    header: "DOWNLOAD",
    cell: ({ row }) => {
      const handleDownload = () => {
        const svg = document.querySelector(`[data-qr-id="${row.original.id}"]`);
        if (!svg) return;
  
        const scaleFactor = 10; // Increase for higher resolution (e.g., 2 = 2x, 3 = 3x, etc.)
  
        const canvas = document.createElement("canvas");
        const ctx = canvas.getContext("2d");
  
        const data = new XMLSerializer().serializeToString(svg);
        const DOMURL = window.URL || window.webkitURL || window;
  
        const svgBlob = new Blob([data], { type: "image/svg+xml;charset=utf-8" });
        const url = DOMURL.createObjectURL(svgBlob);
  
        const img = new Image();
        img.onload = () => {
          // Scale canvas to improve resolution
          const width = img.width * scaleFactor;
          const height = img.height * scaleFactor;
  
          canvas.width = width;
          canvas.height = height;
  
          // Draw image at a higher resolution
          ctx?.drawImage(img, 0, 0, width, height);
          DOMURL.revokeObjectURL(url);
  
          // Convert to PNG with higher quality
          canvas.toBlob((blob) => {
            if (blob) {
              const downloadUrl = DOMURL.createObjectURL(blob);
              const a = document.createElement("a");
              a.href = downloadUrl;
              a.download = `qr-code-${row.original.id}.png`;
              document.body.appendChild(a);
              a.click();
              document.body.removeChild(a);
              DOMURL.revokeObjectURL(downloadUrl);
            }
          }, "image/png");
        };
        img.onerror = (error) => {
          console.error("Failed to load SVG image for download:", error);
        };
        img.src = url;
      };
  
      return (
        <Button
          onClick={handleDownload}
          className="rounded px-2 py-1 text-sm hover:bg-gray-100"
        >
          Download PNG
        </Button>
      );
    },
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
