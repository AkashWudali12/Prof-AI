"use client"

import { useContext, useState, createContext } from "react";

const ShareDataContext = createContext()

export function ShareDataProvider({children}) {
    const [shareData, setShareData] = useState(null)

    return (
        <ShareDataContext.Provider value={{shareData, setShareData}}>
            {children}
        </ShareDataContext.Provider>
    )
}

export function useShareDataContext() {
    return useContext(ShareDataContext)
}