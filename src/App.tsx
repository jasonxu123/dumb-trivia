import { Button, Icon, styled } from '@mui/material';
import { Box } from '@mui/system';
import React from 'react';

// TODO: use process.env.NODE_ENV for production or dev API routes

const GlobalWrapper = styled('div')(
  ({ theme }) => `
  color: ${theme.palette.text.primary};
  font-family: ${theme.typography.fontFamily};
`,
);

const ButtonRow = styled('div')(`
  padding: 16px;
  display: flex;
  flex-direction: row;
  gap: 8px;
  align-items: center;
`);

export const App = () => (
  <GlobalWrapper>
    <Box sx={{ color: 'text.primary', fontSize: 34, fontWeight: 'medium' }}>
      Test that sheets work
    </Box>
    <ButtonRow>
      <Icon>star</Icon>
      <Button variant="contained" disableElevation>
        Test the thing
      </Button>
    </ButtonRow>
    <div>{process.env.NODE_ENV}</div>
  </GlobalWrapper>
);
