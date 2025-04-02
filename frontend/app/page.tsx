'use client';

import { useState } from 'react';
import HeaderNav from '@/components/HeaderNav';
import {
  Box,
  Container,
  Heading,
  Input,
  Button,
  VStack,
  Text,
  Divider,
  Card,
  CardBody,
  Flex,
  Spinner,
} from '@chakra-ui/react';
import { queryLaws } from '@/services/apiService';

export default function Page() {
  const [query, setQuery] = useState('');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!query.trim()) return;

    setLoading(true);
    setError('');
    
    try {
      const response = await queryLaws(query);
      setResult(response);
    } catch (err) {
      setError('Failed to get a response. Please try again.');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <Box>
      <HeaderNav signOut={() => {}} />
      <Container maxW="container.lg" py={8}>
        <VStack spacing={8} align="stretch">
          <Heading as="h1" size="xl">Westeros Law Query System</Heading>
          <Text>Ask questions about laws of Westeros and get AI-powered answers with citations.</Text>
          
          <form onSubmit={handleSubmit}>
            <Flex gap={4}>
              <Input 
                placeholder="What happens if I steal from the Sept?" 
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                size="lg"
                flex={1}
              />
              <Button 
                type="submit" 
                colorScheme="purple" 
                size="lg" 
                isLoading={loading}
                loadingText="Searching"
              >
                Search
              </Button>
            </Flex>
          </form>

          {error && (
            <Box p={4} bg="red.50" color="red.600" borderRadius="md">
              {error}
            </Box>
          )}

          {loading && (
            <Box textAlign="center" py={8}>
              <Spinner size="xl" color="purple.500" />
              <Text mt={4}>Searching through Westeros laws...</Text>
            </Box>
          )}

          {result && !loading && (
            <VStack spacing={6} align="stretch">
              <Card>
                <CardBody>
                  <Heading size="md" mb={2}>Your Query</Heading>
                  <Text>{result.query}</Text>
                </CardBody>
              </Card>

              <Card>
                <CardBody>
                  <Heading size="md" mb={4}>Response</Heading>
                  <Text>{result.response}</Text>
                </CardBody>
              </Card>

              {result.citations && result.citations.length > 0 && (
                <Card>
                  <CardBody>
                    <Heading size="md" mb={4}>Citations</Heading>
                    <VStack spacing={4} align="stretch">
                      {result.citations.map((citation, index) => (
                        <Box key={index} p={4} borderWidth="1px" borderRadius="md">
                          <Text fontWeight="bold">{citation.source}</Text>
                          <Divider my={2} />
                          <Text>{citation.text}</Text>
                        </Box>
                      ))}
                    </VStack>
                  </CardBody>
                </Card>
              )}
            </VStack>
          )}
        </VStack>
      </Container>
    </Box>
  );
}
