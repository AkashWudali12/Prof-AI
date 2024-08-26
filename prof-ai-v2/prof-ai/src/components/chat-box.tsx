'use client'

import { Select, SelectTrigger, SelectContent, SelectItem, SelectPortal, SelectViewport } from "@radix-ui/react-select"
import { Button } from "@/components/ui/button"
import { useRouter } from 'next/navigation';
import { useState } from 'react';
import { LoadingSpinner } from './loading'; 
import { useEffect } from "react";
import { useShareDataContext } from "@/context/SharedDataContext";

export function ChatBox() {
  const router = useRouter();
  const { shareData, setShareData } = useShareDataContext();
  const [selectedOption, setSelectedOption] = useState<string | null>(null);
  const [grade, setGrade] = useState<string>("");
  const [name, setName] = useState<string>("");
  const [school, setSchool] = useState<string>("");
  const [loading, setLoading] = useState(false); // Loading state
  const [message, setMessage] = useState<string>("")

  console.log("Share Data:", shareData);

  useEffect(() => {
    console.log("Selected Option:", selectedOption);
  }, [selectedOption]);

  const handleOptionChange = (value: string) => {
    console.log("Change Selected Option To:", value);
    if (value) setSelectedOption(value);
  };

  const handleGradeChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setGrade(event.target.value)
    console.log("Grade:", event.target.value);
  };

  const handleNameChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setName(event.target.value);
    console.log("Name:", event.target.value);
  };

  const handleSchoolChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setSchool(event.target.value);
    console.log("School:", event.target.value);
  };

  const handleMessageChange = (event: React.ChangeEvent<HTMLTextAreaElement>) => {
    setMessage(event.target.value)
  }

  const handleSubmit = async (event: React.FormEvent) => {
    event.preventDefault();

    const formData = new FormData();
    if (selectedOption && selectedOption != "Select a school") formData.append('university', selectedOption);
    if (message) formData.append("message", message)
    const studentInfo: string[] | Blob = []
    if (name) studentInfo.push(name)
    if (grade) studentInfo.push(grade)
    if (school) studentInfo.push(school)

    if (message && studentInfo.length == 3 && selectedOption && selectedOption != "Select a school") {
      formData.append("studentName", name)
      formData.append("studentGrade", grade)
      formData.append("studentSchool", school)

      setLoading(true); // Show loading spinner

      console.log("Selected Option:", selectedOption);
      console.log("Message:", message)

      try {
        const response = await fetch('https://prof-ai-579919193707.us-east4.run.app/get_professor_description', {
            method: 'POST',
            body: formData
        });
        if (response.ok) {
          const data = await response.json();
          console.log('Server response:', data.response);
      
          setSelectedOption(''); // Reset dropdown after submission
          setShareData({"data":data.response})
          router.push(`/email`);
        }
        else {
          console.error('Error sending message from response:', response);
          setSelectedOption(''); // Reset dropdown after submission
        }
      } catch (error) {
          console.error('Error sending message:', error);
          setSelectedOption(''); // Reset dropdown after submission
      }

      setLoading(false); // Hide loading spinner
    }
  };

  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-background">
      <div className="max-w-md w-full px-6 py-8 bg-card rounded-lg shadow-lg">
        {loading ? (
          <LoadingSpinner /> // Show loading spinner if loading state is true
        ) : (
          <>
            <form onSubmit={handleSubmit} className="flex flex-col gap-4">
              <div className="flex flex-col gap-2">
                <div className="flex items-center justify-between">
                  <div className="flex flex-col gap-1">
                    <h1 className="text-2xl font-bold text-card-foreground">Prof.AI</h1>
                    <p className="text-sm text-muted-foreground">
                      Select your research interest from the dropdown or upload your resume as a PDF.
                    </p>
                  </div>
                </div>

                {/* Student's Name Input */}
                <div className="flex flex-col gap-2">
                  <label htmlFor="name" className="text-sm text-muted-foreground">Name</label>
                  <input
                    type="text"
                    id="name"
                    value={name}
                    onChange={handleNameChange}
                    className="w-full rounded-lg border border-input bg-background text-foreground px-4 py-2"
                    placeholder="Enter your name"
                  />
                </div>

                {/* Student's School Input */}
                <div className="flex flex-col gap-2">
                  <label htmlFor="school" className="text-sm text-muted-foreground">School</label>
                  <input
                    type="text"
                    id="school"
                    value={school}
                    onChange={handleSchoolChange}
                    className="w-full rounded-lg border border-input bg-background text-foreground px-4 py-2"
                    placeholder="Enter your school"
                  />
                </div>

                {/* Student's Grade Selection */}
                <div className="flex flex-col gap-2">
                  <label htmlFor="school" className="text-sm text-muted-foreground">Grade Level</label>
                  <input
                    type="text"
                    id="grade"
                    value={grade}
                    onChange={handleGradeChange}
                    className="w-full rounded-lg border border-input bg-background text-foreground px-4 py-2"
                    placeholder="Enter your grade level"
                  />
                </div>

                {/* Textarea and Send Button */}
                <div className="flex flex-col gap-4">
                  <div className="relative">
                    <textarea
                      placeholder="Type your message..."
                      className="w-full rounded-lg border border-input bg-background text-foreground px-4 py-2 pr-16 focus:outline-none focus:ring-1 focus:ring-primary"
                      rows={4}
                      onChange={handleMessageChange}
                    />
                    <Button
                      type="submit"
                      size="icon"
                      className="absolute top-1/2 -translate-y-1/2 right-3 text-muted-foreground hover:text-foreground"
                    >
                      <SendIcon className="w-5 h-5" />
                      <span className="sr-only">Send</span>
                    </Button>
                  </div>
                </div>

                {/* Select a school */}
                <div className="flex flex-col gap-4">
                  <div className="relative flex-grow">
                    <Select onValueChange={handleOptionChange} value={selectedOption ? selectedOption : "Select a school"}>
                      <SelectTrigger className="w-full rounded-lg border border-input bg-background text-foreground px-4 py-2 pr-16 focus:outline-none focus:ring-1 focus:ring-primary">
                        {selectedOption ? selectedOption : "Select a school"}
                      </SelectTrigger>
                      <SelectContent>
                        <SelectViewport className="max-h-40 overflow-y-auto select-content-overlay">
                          <SelectItem value="Select a school">
                            <p className="text-sm text-muted-foreground" style={{ backgroundColor: '#f0f0f0' }}> Select a school </p>
                          </SelectItem>
                          <SelectItem value="UMD">
                            <p className="text-sm text-muted-foreground" style={{ backgroundColor: '#f0f0f0' }}> University of Maryland - College Park </p>
                          </SelectItem>
                        </SelectViewport>
                      </SelectContent>
                    </Select>
                  </div>
                </div>
              </div>
            </form>
            <p className="text-sm text-muted-foreground text-center mt-4">More schools coming soon!</p>
          </>
        )}
      </div>
    </div>
  )
}

interface IconProps extends React.SVGProps<SVGSVGElement> {}

function SendIcon(props: IconProps) {
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
      <path d="m22 2-7 20-4-9-9-4Z" />
      <path d="M22 2 11 13" />
    </svg>
  )
}

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

export const ChevronDownIcon: React.FC<IconProps> = (props) => {
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
      <polyline points="6 9 12 15 18 9" />
    </svg>
  );
};

export const ChevronUpIcon: React.FC<IconProps> = (props) => {
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
      <polyline points="18 15 12 9 6 15" />
    </svg>
  );
};

