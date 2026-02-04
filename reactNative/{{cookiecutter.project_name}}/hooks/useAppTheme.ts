import { useState, useEffect } from 'react';
import { getAnInformationSync, getAnInformation } from '@/hooks/useInformations';
import { useSession } from '@/hooks/ctx';

export const useAppTheme = () => {
    const { session } = useSession();
    
    const [theme, setTheme] = useState({
        bgcol: getAnInformationSync("bgcol") || "white",
        app_color: getAnInformationSync("app_color") || "#6A52ED",
        text_color: getAnInformationSync("text_color") || "#14315A",
    });

    useEffect(() => {
        const loadTheme = async () => {
            const bgcol = await getAnInformation("bgcol") || "white";
            const app_color = await getAnInformation("app_color") || "#6A52ED";
            const text_color = await getAnInformation("text_color") || "#14315A";

            setTheme({
                bgcol,
                app_color,
                text_color,
            });
        };

        loadTheme();
    }, [session]); // Refresh when session changes

    return theme;
};