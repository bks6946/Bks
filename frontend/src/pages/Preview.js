import React, { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import axios from "axios";
import { Button } from "../components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "../components/ui/card";
import { Badge } from "../components/ui/badge";
import { ArrowLeft, Download, BookOpen, ChevronRight, ChevronLeft } from "lucide-react";

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const Preview = () => {
  const [currentChapter, setCurrentChapter] = useState(0);
  const [ebookContent, setEbookContent] = useState(null);
  const [isGenerating, setIsGenerating] = useState(false);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchEbookContent = async () => {
      try {
        const response = await axios.get(`${API}/ebook/content`);
        setEbookContent(response.data.data);
      } catch (error) {
        console.error('Error fetching ebook content:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchEbookContent();
  }, []);

  const handleDownload = async () => {
    if (isGenerating) return;
    
    setIsGenerating(true);
    
    try {
      const response = await axios.post(`${API}/generate-pdf`);
      
      if (response.data.success) {
        // Create download link
        const downloadUrl = `${BACKEND_URL}${response.data.download_url}`;
        const link = document.createElement('a');
        link.href = downloadUrl;
        link.download = response.data.filename;
        link.click();
      }
    } catch (error) {
      console.error('Error generating PDF:', error);
      alert('Erreur lors de la génération du PDF. Veuillez réessayer.');
    } finally {
      setIsGenerating(false);
    }
  };

  const nextChapter = () => {
    if (ebookContent && currentChapter < ebookContent.chapters.length - 1) {
      setCurrentChapter(currentChapter + 1);
    }
  };

  const prevChapter = () => {
    if (currentChapter > 0) {
      setCurrentChapter(currentChapter - 1);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-indigo-600 mx-auto mb-4"></div>
          <p className="text-gray-600">Chargement...</p>
        </div>
      </div>
    );
  }

  if (!ebookContent) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <p className="text-gray-600">Erreur lors du chargement du contenu</p>
        </div>
      </div>
    );
  }

  const currentChapterData = ebookContent.chapters[currentChapter];

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm">
        <div className="container mx-auto px-4 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-4">
              <Link to="/" className="flex items-center space-x-2 text-gray-600 hover:text-indigo-600 transition-colors">
                <ArrowLeft className="h-5 w-5" />
                <span>Retour</span>
              </Link>
              <div className="flex items-center space-x-2">
                <BookOpen className="h-8 w-8 text-indigo-600" />
                <h1 className="text-2xl font-bold text-gray-900">Aperçu de l'Ebook</h1>
              </div>
            </div>
            <Button 
              onClick={handleDownload} 
              disabled={isGenerating}
              className="bg-indigo-600 hover:bg-indigo-700"
            >
              {isGenerating ? (
                <>
                  <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2"></div>
                  Génération...
                </>
              ) : (
                <>
                  <Download className="mr-2 h-4 w-4" />
                  Télécharger PDF
                </>
              )}
            </Button>
          </div>
        </div>
      </header>

      <div className="container mx-auto px-4 py-8">
        <div className="max-w-6xl mx-auto">
          <div className="grid lg:grid-cols-4 gap-8">
            {/* Sidebar - Table of Contents */}
            <div className="lg:col-span-1">
              <Card className="sticky top-8">
                <CardHeader>
                  <CardTitle className="text-lg">Table des Matières</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="space-y-2">
                    {ebookContent.chapters.map((chapter, index) => (
                      <button
                        key={index}
                        onClick={() => setCurrentChapter(index)}
                        className={`w-full text-left p-2 rounded-lg transition-colors ${
                          currentChapter === index
                            ? 'bg-indigo-100 text-indigo-700 border-l-4 border-indigo-500'
                            : 'hover:bg-gray-50 text-gray-700'
                        }`}
                      >
                        <div className="font-medium text-sm">{chapter.title}</div>
                        <div className="text-xs text-gray-500 mt-1">
                          Chapitre {index + 1}
                        </div>
                      </button>
                    ))}
                  </div>
                </CardContent>
              </Card>
            </div>

            {/* Main Content */}
            <div className="lg:col-span-3">
              <Card>
                <CardHeader>
                  <div className="flex items-center justify-between">
                    <Badge variant="outline" className="mb-2">
                      Chapitre {currentChapter + 1} sur {ebookContent.chapters.length}
                    </Badge>
                    <div className="flex space-x-2">
                      <Button
                        variant="outline"
                        size="sm"
                        onClick={prevChapter}
                        disabled={currentChapter === 0}
                      >
                        <ChevronLeft className="h-4 w-4" />
                      </Button>
                      <Button
                        variant="outline"
                        size="sm"
                        onClick={nextChapter}
                        disabled={currentChapter === ebookContent.chapters.length - 1}
                      >
                        <ChevronRight className="h-4 w-4" />
                      </Button>
                    </div>
                  </div>
                  <CardTitle className="text-2xl">{currentChapterData.title}</CardTitle>
                  <CardDescription>{currentChapterData.description}</CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="prose max-w-none">
                    <div className="space-y-6">
                      {currentChapterData.content.map((section, index) => (
                        <div key={index}>
                          <h3 className="text-lg font-semibold text-gray-900 mb-3">
                            {section.subtitle}
                          </h3>
                          <div className="text-gray-700 space-y-3">
                            {section.text.map((paragraph, pIndex) => (
                              <p key={pIndex} className="leading-relaxed">
                                {paragraph}
                              </p>
                            ))}
                          </div>
                          {section.tips && (
                            <div className="bg-blue-50 border-l-4 border-blue-400 p-4 mt-4">
                              <div className="flex">
                                <div className="ml-3">
                                  <p className="text-sm font-medium text-blue-800">
                                    💡 Conseil Pro :
                                  </p>
                                  <p className="text-sm text-blue-700 mt-1">
                                    {section.tips}
                                  </p>
                                </div>
                              </div>
                            </div>
                          )}
                        </div>
                      ))}
                    </div>
                  </div>
                </CardContent>
              </Card>

              {/* Navigation */}
              <div className="flex justify-between items-center mt-8">
                <Button
                  variant="outline"
                  onClick={prevChapter}
                  disabled={currentChapter === 0}
                  className="flex items-center space-x-2"
                >
                  <ChevronLeft className="h-4 w-4" />
                  <span>Chapitre Précédent</span>
                </Button>
                
                <div className="text-sm text-gray-500">
                  {currentChapter + 1} / {ebookContent.chapters.length}
                </div>
                
                <Button
                  variant="outline"
                  onClick={nextChapter}
                  disabled={currentChapter === ebookContent.chapters.length - 1}
                  className="flex items-center space-x-2"
                >
                  <span>Chapitre Suivant</span>
                  <ChevronRight className="h-4 w-4" />
                </Button>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* CTA Section */}
      <section className="bg-indigo-600 py-12 mt-16">
        <div className="container mx-auto px-4 text-center">
          <h3 className="text-2xl font-bold text-white mb-4">
            Vous aimez ce que vous lisez ?
          </h3>
          <p className="text-indigo-100 mb-6 max-w-2xl mx-auto">
            Téléchargez l'ebook complet avec tous les chapitres, exercices pratiques et bonus exclusifs.
          </p>
          <Button 
            size="lg" 
            onClick={handleDownload}
            disabled={isGenerating}
            className="bg-white text-indigo-600 hover:bg-gray-50 px-8 py-3"
          >
            {isGenerating ? (
              <>
                <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-indigo-600 mr-2"></div>
                Génération...
              </>
            ) : (
              <>
                <Download className="mr-2 h-5 w-5" />
                Télécharger l'Ebook Complet
              </>
            )}
          </Button>
        </div>
      </section>
    </div>
  );
};

export default Preview;