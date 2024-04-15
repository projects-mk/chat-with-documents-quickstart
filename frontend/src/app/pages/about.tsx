
import {
    Card,
    CardContent,
    CardDescription,
    CardFooter,
    CardHeader,
    CardTitle,
  } from "@/components/ui/card"

import { Separator } from "@/components/ui/separator"

function About() {
    return (
        <Card className="mx-auto w-full mt-7 max-w-[900px] min-w-[700px]">
            <CardHeader>
                <CardTitle className="text-xlg">About this application</CardTitle>
                <CardDescription className="text-xlg">
                    Ask questions, get answers, and share your knowledge with others.
                </CardDescription>
            </CardHeader>

            <CardContent className="space-y-2">
                <div className="space-y-4">
                    <CardTitle className="text-xlg">Technologies</CardTitle>
                    <CardDescription className="text-xlg">
                        <ul>
                            <li> <strong>Fontend</strong> - React, Next.js, Tailwind CSS</li>
                            <li> <strong>Backend</strong>  - Python, FastAPI, Ollama, Postres</li>
                        </ul>
                    </CardDescription>
                </div>
            </CardContent>
        </Card>
    )
}

export { About }

