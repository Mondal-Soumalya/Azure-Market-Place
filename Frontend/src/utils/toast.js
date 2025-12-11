// src/utils/toast.js
import { toast } from "react-toastify";

const DEFAULT = {
  position: "top-right",
  autoClose: 3000,
  hideProgressBar: false,
  closeOnClick: true,
  pauseOnHover: true,
  draggable: true,
  theme: "colored",
};

export const success = (msg, opts = {}) => toast.success(msg, { ...DEFAULT, ...opts });
export const error = (msg, opts = {}) => toast.error(msg, { ...DEFAULT, ...opts });
export const info = (msg, opts = {}) => toast.info(msg, { ...DEFAULT, ...opts });
export const warn = (msg, opts = {}) => toast.warn(msg, { ...DEFAULT, ...opts });

export default { success, error, info, warn };
