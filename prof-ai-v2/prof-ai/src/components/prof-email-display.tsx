'use client'

import { useRouter } from 'next/navigation';
import { useEffect, useState, useRef } from 'react';
import { Carousel, CarouselPrevious, CarouselContent, CarouselItem, CarouselNext } from "@/components/ui/carousel"
import { Button } from "@/components/ui/button"
import { Professor } from "./types/professor";
import { useShareDataContext } from '@/context/SharedDataContext';
import type { CarouselApi } from "@/components/ui/carousel" 
import { LoadingSpinner } from './loading';
import React from 'react';


type StringArrayDictionary = { [key: string]: string[] };


export function ProfEmailDisplay() {
  const { shareData, setShareData } = useShareDataContext()
  const router = useRouter(); // Add useRouter hook
  const [professors, setProfessors] = useState<Professor[]>([]);
  const [api, setApi] = useState<CarouselApi>()
  const [abstractsDct, setAbstractDct] = useState<StringArrayDictionary>({})
  const [studentInfo, setStudentInfo] = useState<String[]>([])
  const [currEmail, setCurrEmail] = useState("")
  const [currSubjectLine, setCurrSubjectLine] = useState("")
  const [loading, setLoading] = useState(false);

  const [copiedEmail, setCopiedEmail] = useState(false)
  const [copiedAddress, setCopiedAddress] = useState(false)
  const [copiedSubject, setCopiedSubject] = useState(false)

  const [file, setFile] = useState<File | null>(null);
  const [fileName, setFileName] = useState<string | null>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);



  function delay(ms: number) {
    return new Promise(resolve => setTimeout(resolve, ms));
  }
  

  useEffect(() => {
    if (shareData && professors.length === 0) {
      const data = shareData["data"]
      const abstracts_and_info = data["abstracts_and_info_by_id"]
      const descriptions = data["descriptions_by_id"]
      const profs : Professor[] = []

      const student_to_add: string[] = data["student_info"]
      setStudentInfo(student_to_add)


      const prof_to_abstracts: StringArrayDictionary = {}

      // make list that maps indexes of carousel to ids
      // use that to select the correct id when generating the email

      for (const prof_id in abstracts_and_info) {
        if (prof_id in descriptions) {
          const abstracts: string[] = abstracts_and_info[prof_id][0]
          const info = abstracts_and_info[prof_id][1]

          prof_to_abstracts[prof_id] = abstracts

          const last_first = info["Name"].split(", ")
          const name = "Professor " + last_first[1] + " " + last_first[0]
          const email = info["Email"]
          const picture = info["Picture URL"]
          const description = descriptions[prof_id]

          const withoutdash = description.split("- ")
          var withoutnewline = []
          for (const idx in withoutdash) { // inefficient can improve later
            const str = withoutdash[idx]
            withoutnewline.push(str.replace("\n", ""))
          }

          profs.push({name:name, image_file_path:picture, email: email, description: withoutnewline})

          setAbstractDct(prof_to_abstracts)
        }
      }
      setProfessors(profs)
    }
  }, [shareData]);

  useEffect(() => {
    if (!api) {
      return
    }

    // You can now use the api here
    console.log("Current slide:", api.selectedScrollSnap())
  }, [api])

  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    if (event.target.files && event.target.files[0]) {
      setFile(event.target.files[0]);
      setFileName(event.target.files[0].name);
    }
  };

  const handleUploadClick = () => {
    if (fileInputRef.current) {
      fileInputRef.current.click();
    }
  };

  const handleGenerateEmail = async () => {
    var abstract_list: string[] = []
    if (api) {
      console.log("File:", file)
      console.log("File Name:", fileName)

      const currentIndex = api.selectedScrollSnap();
      const currentProfessor = professors[currentIndex];
      console.log("Generating email for:", currentProfessor.name);
      console.log("studentInfo:", studentInfo)

      const keys = Object.keys(abstractsDct)
      const currKey = keys[currentIndex]
      abstract_list = abstractsDct[currKey]

      const formData = new FormData()

      if (file) {
        setLoading(true)

        formData.append("file", file)

        try {
          const response = await fetch('http://127.0.0.1:5000/get_resume_text', {
            method: 'POST',
            body: formData
          });
          const result = await response.json()
          if (response.ok) {
            const resumeText = result["resumeText"]

            console.log(resumeText)

            try {
              const response = await fetch('http://127.0.0.1:5000/generate_email', {
                  method: 'POST',
                  headers: {
                      'Content-Type': 'application/json'
                  },
                  body: JSON.stringify({"list": abstract_list, "name":currentProfessor.name, "student_info":studentInfo, "resumeText":resumeText})
              });
              const result = await response.json();
              if (response.ok) {
                console.log("Email:", result["email"]);
                const subjectLine = result["email"].split("\n\n")[0]
                setCurrSubjectLine(subjectLine)
                setCurrEmail(result["email"].replace(subjectLine, ""))
              }
              else {
                console.log("Error:", result["error"])
              }
            } 
            catch (error) {
                console.error("Error sending data to backend:", error);
            }
          }
          else {
            console.log("Error:", result["error"])
          }
        }
        catch (error) {
          console.error("Error getting resume text:", error);
        }

        setLoading(false)
      }
      else {
        alert("Please attach your resume.")
      }
    }

  };

  const copyEmail = async () => {
    navigator.clipboard.writeText(currEmail)
    setCopiedEmail(true)
    await delay(1500);
    setCopiedEmail(false)
  }

  const copySubject = async () => {
    navigator.clipboard.writeText(currSubjectLine)
    setCopiedSubject(true)
    await delay(1500);
    setCopiedSubject(false)
  }

  const copyAddress = async () => {
    navigator.clipboard.writeText(professors ? professors[api ? api.selectedScrollSnap() : 0].email : "Example@school.edu")
    setCopiedAddress(true)
    await delay(1500)
    setCopiedAddress(false)
  }

  function formatEmailContent(emailString: string, subjectLineString: string) {
    // Split the string into paragraphs based on double newlines
    const paragraphs = emailString.split('\n\n');
  
    return (
      <div style={{ marginTop: '16px' }}>
        {/* Subject line with copy button */}
        <div style={{ display: 'flex', alignItems: 'center', marginBottom: '16px' }}>
          <p style={{ fontWeight: 'bold', marginRight: '8px' }}>{subjectLineString}</p>
          <Button variant="outline" className="text-muted-foreground hover:text-foreground" onClick={copySubject}>
            {copiedSubject ? (<CheckIcon /> ) : (<CopyIcon className="w-5 h-5" />)}
          </Button>
        </div>
  
        {/* Map each paragraph to a <p> tag */}
        {paragraphs.slice(1).map((paragraph, index) => (
          <p key={index}>
            {paragraph.split('\n').map((line, lineIndex) => (
              <React.Fragment key={lineIndex}>
                {line}
                {lineIndex < paragraph.split('\n').length - 1 && <br />}
              </React.Fragment>
            ))}
          </p>
        ))}
      </div>
    );
  }

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 gap-8 w-full max-w-6xl mx-auto py-12 px-4 md:px-6">
      <div className="relative flex flex-col items-start">
        <Carousel className="w-full rounded-xl overflow-hidden" setApi={setApi}>
          <CarouselPrevious className="absolute left-4 top-1/2 -translate-y-1/2 z-10 text-muted-foreground hover:text-primary-foreground">
            <ChevronLeftIcon className="w-6 h-6" />
          </CarouselPrevious>
          <CarouselContent>
            {professors.map((professor, index) => (
              <CarouselItem key={index}>
                <div className="flex flex-col gap-4 p-6 bg-muted rounded-xl">
                  <h2 className="text-3xl font-bold">{professor.name}</h2> {/* Name */}
                  <div className="flex gap-4 items-start"> {/* Flex container with fixed-size image */}
                    <img
                      src={professor.image_file_path}
                      alt="Professor Image Placeholder"
                      className="rounded-xl object-cover"
                      style={{ width: '200px', height: '150px' }} // Fixed size for the image
                    />
                    <p className="text-base text-muted-foreground flex-grow">
                      {professor.description[0]}
                      {professor.description.slice(1).map((str, index) => (
                        <li key={index}>{str}</li>
                      ))}
                    </p>
                  </div>
                </div>
              </CarouselItem>
            ))}
          </CarouselContent>
          <CarouselNext className="absolute right-4 top-1/2 -translate-y-1/2 z-10 text-muted-foreground hover:text-primary-foreground">
            <ChevronRightIcon className="w-6 h-6" />
          </CarouselNext>
        </Carousel>
      </div>

      {loading ? (<LoadingSpinner />) : (
        <div className="flex flex-col items-start gap-6 relative">
          <div className="bg-muted p-6 rounded-xl w-full">
            <div className="flex justify-between items-center">
              <h3 className="text-xl font-semibold text-muted-foreground">
                {professors.length > 0 ? professors[api ? api.selectedScrollSnap() : 0].email : "Example@school.edu"}
              </h3>
              <Button variant="outline" className="text-muted-foreground hover:text-foreground" onClick={copyAddress}>
                {copiedAddress ? (<CheckIcon /> ) : (<CopyIcon className="w-5 h-5" />)}
              </Button>
            </div>

            <div className="mt-8">
            <div className="flex justify-between items-center">
              <h3 className="text-xl font-semibold text-muted-foreground">
                Cold Email
              </h3>
              <Button variant="outline" className="text-muted-foreground hover:text-foreground" onClick={copyEmail}>
                {copiedEmail ? (<CheckIcon /> ) : (<CopyIcon className="w-5 h-5" />)}
              </Button>
            </div>
            <div className="prose text-muted-foreground">
              {currEmail ? formatEmailContent(currEmail, currSubjectLine) : (
                <div>
                  <p>Dear [Prospect Name],</p>
                  <p>
                    I hope this email finds you well. My name is [Your Name], and I work at [Your Company]. I came across your
                    profile and was impressed by your work in [Relevant Industry/Field].
                  </p>
                  <p>
                    I believe our [Product/Service] could be a great fit for your [Prospect's Pain Point]. We've helped
                    similar businesses like yours [Relevant Benefit] and I'd love the opportunity to discuss how we can do the
                    same for you.
                  </p>
                  <p>
                    Would you be available for a quick call this week to learn more? I'm flexible and can work around your
                    schedule.
                  </p>
                  <p>Thank you for your time, and I look forward to connecting.</p>
                  <p>
                    Best regards,
                    <br />
                    [Your Name]
                    <br />
                    [Your Company]
                  </p>
                </div>
              )}
            </div>
            <div className="relative flex flex-col items-start">
            <div className="flex items-center gap-4 w-full mt-4">
              <Button className="flex-grow" onClick={handleGenerateEmail}>
                Generate Email
              </Button>
              <div className="flex items-center">
                <button
                  type="button"
                  className="text-primary-foreground hover:text-primary transition-colors"
                  onClick={handleUploadClick}
                >
                  <UploadIcon className="w-5 h-5" />
                  <span className="sr-only">Upload PDF</span>
                </button>
                <input
                  type="file"
                  accept="application/pdf"
                  ref={fileInputRef}
                  className="hidden"
                  onChange={handleFileChange}
                />
                {fileName && (
                  <p className="text-sm text-muted-foreground ml-2">{fileName}</p>
                )}
              </div>
            </div>
          </div>
          </div>
        </div>
      </div>
    )}
  </div>
  )
}

interface IconProps extends React.SVGProps<SVGSVGElement> {}

function ChevronLeftIcon(props: IconProps) {
  return (
    <svg
      {...props}
      xmlns="http://www.w3.org/2000/svg"
      width="24"
      height="24"
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="2"
      strokeLinecap="round"
      strokeLinejoin="round"
    >
      <path d="m15 18-6-6 6-6" />
    </svg>
  )
}

function ChevronRightIcon(props: IconProps) {
  return (
    <svg
      {...props}
      xmlns="http://www.w3.org/2000/svg"
      width="24"
      height="24"
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="2"
      strokeLinecap="round"
      strokeLinejoin="round"
    >
      <path d="m9 18 6-6-6-6" />
    </svg>
  )
}

function CopyIcon(props: IconProps) {
  return (
    <svg
      {...props}
      xmlns="http://www.w3.org/2000/svg"
      width="24"
      height="24"
      viewBox="0 0 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="2"
      strokeLinecap="round"
      strokeLinejoin="round"
    >
      <rect width="14" height="14" x="8" y="8" rx="2" ry="2" />
      <path d="M4 16c-1.1 0-2-.9-2-2V4c0-1.1.9-2 2-2h10c1.1 0 2 .9 2 2" />
    </svg>
  )
}

const CheckIcon: React.FC = () => (
  <svg
    xmlns="http://www.w3.org/2000/svg"
    width="16"
    height="16"
    fill="green"
    viewBox="0 0 16 16"
  >
    <path d="M13.485 1.929a1.5 1.5 0 10-2.121-2.121L6 5.172l-1.364-1.364a1.5 1.5 0 00-2.122 2.122L5.879 9.414l7.606-7.485z" />
  </svg>
);

function UploadIcon(props: IconProps) {
  return (
    <svg
      {...props}
      xmlns="http://www.w3.org/2000/svg"
      width="24"
      height="24"
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="2"
      strokeLinecap="round"
      strokeLinejoin="round"
    >
      <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4" />
      <polyline points="17 8 12 3 7 8" />
      <line x1="12" x2="12" y1="3" y2="15" />
    </svg>
  )
}
