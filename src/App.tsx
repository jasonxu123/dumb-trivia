import { styled } from '@mui/material';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import TestPage from './TestPage';

const API_DOMAIN =
  process.env.NODE_ENV === 'development'
    ? 'http://localhost:3000'
    : 'https://dumb-trivia.vercel.app';

const GlobalWrapper = styled('div')(
  ({ theme }) => `
  color: ${theme.palette.text.primary};
  font-family: ${theme.typography.fontFamily};
`,
);

export const App = () => (
  <GlobalWrapper>
    <Router>
      <Routes>
        <Route path="/" element={<div>Yay, a blank page.</div>} />
        <Route path="test" element={<TestPage apiDomain={API_DOMAIN} />} />
      </Routes>
    </Router>
  </GlobalWrapper>
);
