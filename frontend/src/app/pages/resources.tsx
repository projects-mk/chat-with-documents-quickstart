
import {
    Card,
    CardContent,
    CardDescription,
    CardFooter,
    CardHeader,
    CardTitle,
  } from "@/components/ui/card"

  import { Input } from "@/components/ui/input"

import {
    Table,
    TableBody,
    TableCaption,
    TableCell,
    TableHead,
    TableHeader,
    TableRow,
  } from "@/components/ui/table"

import { Button, buttonVariants, ButtonLink } from "@/components/ui/button"
import Link from "next/link"
import * as React from "react"
import {
  ColumnDef,
  ColumnFiltersState,
  SortingState,
  VisibilityState,
  flexRender,
  getCoreRowModel,
  getFilteredRowModel,
  getPaginationRowModel,
  getSortedRowModel,
  useReactTable,
} from "@tanstack/react-table"

function ResourcesSummary() {
    return (
        <Card className="mx-auto w-full mt-7 max-w-[900px] min-w-[700px]">
            <CardHeader>
                <CardTitle className="text-xlg mb-5">Manage Resources</CardTitle>
            </CardHeader>
            <Table>
                <TableHeader>
                    <TableRow>
                        <TableHead>Resource</TableHead>
                        <TableHead>Status</TableHead>
                    </TableRow>
                </TableHeader>
                <TableBody>
                    <TableRow>
                        <TableCell>Vector Database</TableCell>
                        <TableCell>Connected</TableCell>
                    </TableRow>
                    <TableRow>
                        <TableCell>App Database</TableCell>
                        <TableCell>Connected</TableCell>
                    </TableRow>
                    <TableRow>
                        <TableCell>LLM Monitoring</TableCell>
                        <TableCell>Connected</TableCell>
                    </TableRow>
                </TableBody>
            </Table>
        </Card>
    );
}

function LLMs() {
    return (
        <Card className="mx-auto w-full mt-7 max-w-[900px] min-w-[700px]">
            <CardHeader>
                <CardTitle className="text-xlg mb-5">LLM Selection</CardTitle>
            </CardHeader>
            <CardContent>
                <CardDescription>
                    <div className="flex items-center">
                        Download an open source LLM, complete list can be found 
                        <Button variant="link" className="rounded px-1 py-1 text-sm">
                            <Link href="https://ollama.com/library">here</Link>
                        </Button>
                    </div>
                </CardDescription>
                <div className="flex items-center">
                    <div className="flex w-full max-w-sm items-center space-x-2">
                        <Input type="text" placeholder="Ollama model name " />
                        <Button type="submit">Download</Button>
                    </div>
                </div>
            </CardContent>
        </Card>
    );
}

function Collections() {
    return (
        <Card className="mx-auto w-full mt-7 max-w-[900px] min-w-[700px]">
            <CardHeader>
                <CardTitle className="text-xlg mb-5">Uploaded Documents</CardTitle>
            </CardHeader>
            <CardContent>
                <CardDescription>
                    Below is a list of uploaded documents and their respective collections.
                </CardDescription>
                <div className="flex items-center">

                </div>
            </CardContent>
        </Card>
    );
}

function ManageAllResources() {
  return (
    <div>
    <ResourcesSummary />
    <LLMs />
    <Collections />
    </div>
  );
}


export { ManageAllResources };