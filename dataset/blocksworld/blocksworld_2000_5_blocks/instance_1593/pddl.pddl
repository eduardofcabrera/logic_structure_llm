

(define (problem BW-rand-5)
(:domain blocksworld-4ops)
(:objects a b c d e )
(:init
(handempty)
(on a e)
(ontable b)
(ontable c)
(ontable d)
(on e d)
(clear a)
(clear b)
(clear c)
)
(:goal
(and
(on b a)
(on d c))
)
)


