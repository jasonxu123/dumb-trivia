import { styled } from '@mui/material';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import TestPage from './TestPage';

const API_DOMAIN =
  process.env.NODE_ENV === 'development'
    ? 'http://localhost:3000'
    : 'https://dumb-trivia.vercel.app';
const BASE_ROUTE =
  process.env.NODE_ENV === 'development' ? '/' : '/dumb-trivia';

const GlobalWrapper = styled('div')(
  ({ theme }) => `
  color: ${theme.palette.text.primary};
  font-family: ${theme.typography.fontFamily};
`,
);

export const App = () => (
  <GlobalWrapper>
    <Router basename={BASE_ROUTE}>
      <Routes>
        <Route
          path="/"
          element={<div>Yay, a blank page at route "{BASE_ROUTE}".</div>}
        />
        <Route path="test" element={<TestPage apiDomain={API_DOMAIN} />} />
      </Routes>
    </Router>
  </GlobalWrapper>
);
