import React from "react";
import { Link } from "react-router-dom";
import { Button } from "../components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "../components/ui/card";
import { Badge } from "../components/ui/badge";
import { Download, BookOpen, TrendingUp, Users, Clock, Star } from "lucide-react";
import { mockEbook } from "../data/mock";

const Home = () => {
  const handleDownload = () => {
    // Mock download functionality
    const link = document.createElement('a');
    link.href = '#';
    link.download = 'comment-faire-1000-euros-en-1-mois.pdf';
    link.click();
    alert('Téléchargement commencé ! (Fonctionnalité mock)');
  };

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
              className="bg-indigo-600 hover:bg-indigo-700 text-white px-8 py-4 text-lg"
            >
              <Download className="mr-2 h-5 w-5" />
              Télécharger l'Ebook PDF
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
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-16">
            <Card className="text-center">
              <CardContent className="pt-6">
                <Users className="h-12 w-12 text-indigo-600 mx-auto mb-2" />
                <div className="text-3xl font-bold text-gray-900">15k+</div>
                <div className="text-gray-600">Étudiants aidés</div>
              </CardContent>
            </Card>
            <Card className="text-center">
              <CardContent className="pt-6">
                <TrendingUp className="h-12 w-12 text-green-600 mx-auto mb-2" />
                <div className="text-3xl font-bold text-gray-900">85%</div>
                <div className="text-gray-600">Taux de réussite</div>
              </CardContent>
            </Card>
            <Card className="text-center">
              <CardContent className="pt-6">
                <Clock className="h-12 w-12 text-orange-600 mx-auto mb-2" />
                <div className="text-3xl font-bold text-gray-900">30 jours</div>
                <div className="text-gray-600">Pour voir des résultats</div>
              </CardContent>
            </Card>
          </div>
        </div>
      </section>

      {/* Content Preview */}
      <section className="bg-white py-16">
        <div className="container mx-auto px-4">
          <div className="max-w-4xl mx-auto">
            <h3 className="text-3xl font-bold text-center mb-12">
              Ce que vous allez apprendre
            </h3>
            
            <div className="grid md:grid-cols-2 gap-8">
              {mockEbook.chapters.slice(0, 6).map((chapter, index) => (
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
            {[
              {
                name: "Marie L.",
                role: "Étudiante en Commerce",
                content: "J'ai réussi à gagner 1200€ en suivant les conseils sur le freelancing. Parfait pour financer mes études !",
                rating: 5
              },
              {
                name: "Thomas R.",
                role: "Étudiant en Informatique",
                content: "Les stratégies de vente en ligne m'ont permis de créer un complément de revenus stable. Très pratique !",
                rating: 5
              },
              {
                name: "Sarah M.",
                role: "Étudiante en Droit",
                content: "Guide très complet avec des méthodes réalistes. J'ai pu économiser pour mon voyage d'études.",
                rating: 5
              }
            ].map((testimonial, index) => (
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
            className="bg-white text-indigo-600 hover:bg-gray-50 px-8 py-4 text-lg"
          >
            <Download className="mr-2 h-5 w-5" />
            Télécharger Maintenant - Gratuit
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