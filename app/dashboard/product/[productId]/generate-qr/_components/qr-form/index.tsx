"use client";

import React from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import {
  Form,
  FormControl,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from "@/components/ui/form";
import { zodResolver } from "@hookform/resolvers/zod";
import { useForm } from "react-hook-form";
import * as z from "zod";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";

const QRForm = () => {
  const formSchema = z.object({
    serialNo: z
      .string()
      .max(30, "Serial number should not exceed 30 characters"),
    batchNo: z
      .string()
      .max(30, "Batch number should not exceed 30 characters")
      .optional(),
  });

  const defaultValues = {
    serialNo: "",
    batchNo: "",
  };

  const form = useForm<z.infer<typeof formSchema>>({
    resolver: zodResolver(formSchema),
    values: defaultValues,
  });

  function onSubmit(values: z.infer<typeof formSchema>) {
    console.log(values);
  }

  return (
    <Card className="mx-auto w-full">
      <CardHeader>
        <CardTitle className="text-left text-2xl font-bold">
          Generate QR Code
        </CardTitle>
      </CardHeader>
      <CardContent>
        <Form {...form}>
          <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-8">
            <div className="grid grid-cols-1 gap-6 md:grid-cols-2">
              <FormField
                control={form.control}
                name="serialNo"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>Product Serial No. (or any unique ID)</FormLabel>
                    <FormControl>
                      <Input
                        type="string"
                        step="0.01"
                        placeholder="Enter serial number "
                        {...field}
                      />
                    </FormControl>
                    <FormMessage />
                  </FormItem>
                )}
              />
              <FormField
                control={form.control}
                name="batchNo"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>Enter Batch No.</FormLabel>
                    <FormControl>
                      <Input
                        type="string"
                        step="0.01"
                        placeholder="Enter Batch No"
                        {...field}
                      />
                    </FormControl>
                    <FormMessage />
                  </FormItem>
                )}
              />
            </div>
            <Button type="submit">Generate QR</Button>
          </form>
        </Form>
      </CardContent>
    </Card>
  );
};

export default QRForm;