import React, { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import axios from "axios";
import { Button } from "../components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "../components/ui/card";
import { Badge } from "../components/ui/badge";
import { Download, BookOpen, TrendingUp, Users, Clock, Star } from "lucide-react";

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const Home = () => {
  const [ebookContent, setEbookContent] = useState(null);
  const [stats, setStats] = useState(null);
  const [testimonials, setTestimonials] = useState([]);
  const [isGenerating, setIsGenerating] = useState(false);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [ebookResponse, statsResponse, testimonialsResponse] = await Promise.all([
          axios.get(`${API}/ebook/content`),
          axios.get(`${API}/stats`),
          axios.get(`${API}/testimonials`)
        ]);

        setEbookContent(ebookResponse.data.data);
        setStats(statsResponse.data);
        setTestimonials(testimonialsResponse.data.data);
      } catch (error) {
        console.error('Error fetching data:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
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

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-indigo-600 mx-auto mb-4"></div>
          <p className="text-gray-600">Chargement...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      {/* Header */}
      <header className="bg-white shadow-sm">
        <div className="container mx-auto px-4 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-2">
              <BookOpen className="h-8 w-8 text-indigo-600" />
              <h1 className="text-2xl font-bold text-gray-900">EbookStudent</h1>
            </div>
            <nav className="hidden md:flex space-x-6">
              <Link to="/" className="text-gray-600 hover:text-indigo-600 transition-colors">
                Accueil
              </Link>
              <Link to="/preview" className="text-gray-600 hover:text-indigo-600 transition-colors">
                Aperçu
              </Link>
            </nav>
          </div>
        </div>
      </header>

      {/* Hero Section */}
      <section className="container mx-auto px-4 py-16">
        <div className="max-w-4xl mx-auto text-center">
          <Badge className="mb-4 bg-indigo-100 text-indigo-800 hover:bg-indigo-200">
            🎓 Spécial Étudiants
          </Badge>
          <h2 className="text-4xl md:text-6xl font-bold text-gray-900 mb-6">
            Comment Faire{" "}
            <span className="text-indigo-600">1000€ en 1 Mois</span>{" "}
            en Étant Jeune
          </h2>
          <p className="text-xl text-gray-600 mb-8 max-w-2xl mx-auto">
            Découvrez des méthodes éprouvées et réalistes pour augmenter vos revenus 
            pendant vos études. Guide complet avec stratégies concrètes et étapes détaillées.
          </p>
          
          <div className="flex flex-col sm:flex-row gap-4 justify-center mb-12">
            <Button 
              size="lg" 
              onClick={handleDownload}
              disabled={isGenerating}
              className="bg-indigo-600 hover:bg-indigo-700 text-white px-8 py-4 text-lg"
            >
              {isGenerating ? (
                <>
                  <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white mr-2"></div>
                  Génération en cours...
                </>
              ) : (
                <>
                  <Download className="mr-2 h-5 w-5" />
                  Télécharger l'Ebook PDF
                </>
              )}
            </Button>
            <Button 
              size="lg" 
              variant="outline" 
              asChild
              className="border-indigo-200 text-indigo-600 hover:bg-indigo-50 px-8 py-4 text-lg"
            >
              <Link to="/preview">
                <BookOpen className="mr-2 h-5 w-5" />
                Aperçu Gratuit
              </Link>
            </Button>
          </div>

          {/* Stats */}
          {stats && (
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-16">
              <Card className="text-center">
                <CardContent className="pt-6">
                  <Users className="h-12 w-12 text-indigo-600 mx-auto mb-2" />
                  <div className="text-3xl font-bold text-gray-900">{stats.students_helped.toLocaleString()}+</div>
                  <div className="text-gray-600">Étudiants aidés</div>
                </CardContent>
              </Card>
              <Card className="text-center">
                <CardContent className="pt-6">
                  <TrendingUp className="h-12 w-12 text-green-600 mx-auto mb-2" />
                  <div className="text-3xl font-bold text-gray-900">{stats.success_rate}%</div>
                  <div className="text-gray-600">Taux de réussite</div>
                </CardContent>
              </Card>
              <Card className="text-center">
                <CardContent className="pt-6">
                  <Clock className="h-12 w-12 text-orange-600 mx-auto mb-2" />
                  <div className="text-3xl font-bold text-gray-900">{stats.avg_time_to_results} jours</div>
                  <div className="text-gray-600">Pour voir des résultats</div>
                </CardContent>
              </Card>
            </div>
          )}
        </div>
      </section>

      {/* Content Preview */}
      <section className="bg-white py-16">
        <div className="container mx-auto px-4">
          <div className="max-w-4xl mx-auto">
            <h3 className="text-3xl font-bold text-center mb-12">
              Ce que vous allez apprendre
            </h3>
            
            {ebookContent && (
              <div className="grid md:grid-cols-2 gap-8">
                {ebookContent.chapters.slice(0, 6).map((chapter, index) => (
                  <Card key={index} className="hover:shadow-lg transition-shadow">
                    <CardHeader>
                      <div className="flex items-center space-x-3">
                        <div className="w-8 h-8 bg-indigo-100 rounded-full flex items-center justify-center">
                          <span className="text-indigo-600 font-bold">{index + 1}</span>
                        </div>
                        <CardTitle className="text-lg">{chapter.title}</CardTitle>
                      </div>
                    </CardHeader>
                    <CardContent>
                      <CardDescription className="text-gray-600">
                        {chapter.description}
                      </CardDescription>
                    </CardContent>
                  </Card>
                ))}
              </div>
            )}
          </div>
        </div>
      </section>

      {/* Testimonials */}
      <section className="bg-gray-50 py-16">
        <div className="container mx-auto px-4">
          <h3 className="text-3xl font-bold text-center mb-12">
            Ce que disent nos étudiants
          </h3>
          
          <div className="grid md:grid-cols-3 gap-8 max-w-6xl mx-auto">
            {testimonials.map((testimonial, index) => (
              <Card key={index} className="hover:shadow-lg transition-shadow">
                <CardContent className="pt-6">
                  <div className="flex mb-4">
                    {[...Array(testimonial.rating)].map((_, i) => (
                      <Star key={i} className="h-5 w-5 text-yellow-400 fill-current" />
                    ))}
                  </div>
                  <p className="text-gray-600 mb-4">"{testimonial.content}"</p>
                  <div>
                    <div className="font-semibold text-gray-900">{testimonial.name}</div>
                    <div className="text-sm text-gray-500">{testimonial.role}</div>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="bg-indigo-600 py-16">
        <div className="container mx-auto px-4 text-center">
          <h3 className="text-3xl font-bold text-white mb-4">
            Prêt à augmenter vos revenus ?
          </h3>
          <p className="text-xl text-indigo-100 mb-8 max-w-2xl mx-auto">
            Téléchargez votre guide complet et commencez à générer des revenus dès aujourd'hui.
          </p>
          <Button 
            size="lg" 
            onClick={handleDownload}
            disabled={isGenerating}
            className="bg-white text-indigo-600 hover:bg-gray-50 px-8 py-4 text-lg"
          >
            {isGenerating ? (
              <>
                <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-indigo-600 mr-2"></div>
                Génération...
              </>
            ) : (
              <>
                <Download className="mr-2 h-5 w-5" />
                Télécharger Maintenant - Gratuit
              </>
            )}
          </Button>
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-gray-900 text-white py-12">
        <div className="container mx-auto px-4">
          <div className="grid md:grid-cols-4 gap-8">
            <div>
              <div className="flex items-center space-x-2 mb-4">
                <BookOpen className="h-6 w-6" />
                <span className="text-xl font-bold">EbookStudent</span>
              </div>
              <p className="text-gray-400">
                Ressources éducatives pour étudiants entrepreneurs.
              </p>
            </div>
            <div>
              <h4 className="font-semibold mb-4">Liens Utiles</h4>
              <ul className="space-y-2 text-gray-400">
                <li><Link to="/" className="hover:text-white transition-colors">Accueil</Link></li>
                <li><Link to="/preview" className="hover:text-white transition-colors">Aperçu</Link></li>
              </ul>
            </div>
            <div>
              <h4 className="font-semibold mb-4">Support</h4>
              <ul className="space-y-2 text-gray-400">
                <li><a href="#" className="hover:text-white transition-colors">Contact</a></li>
                <li><a href="#" className="hover:text-white transition-colors">FAQ</a></li>
              </ul>
            </div>
            <div>
              <h4 className="font-semibold mb-4">Légal</h4>
              <ul className="space-y-2 text-gray-400">
                <li><a href="#" className="hover:text-white transition-colors">Mentions Légales</a></li>
                <li><a href="#" className="hover:text-white transition-colors">Confidentialité</a></li>
              </ul>
            </div>
          </div>
          <div className="border-t border-gray-800 mt-8 pt-8 text-center text-gray-400">
            <p>&copy; 2025 EbookStudent. Tous droits réservés.</p>
          </div>
        </div>
      </footer>
    </div>
  );
};

export default Home;