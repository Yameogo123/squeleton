

import Toast from "react-native-toast-message";

export function useErrorToast(content:string) {
  Toast.show({ type: 'error', text1: 'Erreur survenue!', text2: content });
}

export function useWarningToast(content:string) {
    Toast.show({ type: 'info', text1: 'Attention!', text2: content });
}

export function useSuccessToast(content:string) {
    Toast.show({ type: 'success', text1: 'Bravo!', text2: content });
}