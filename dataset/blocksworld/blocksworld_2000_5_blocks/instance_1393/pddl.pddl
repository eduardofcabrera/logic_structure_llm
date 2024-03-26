

(define (problem BW-rand-5)
(:domain blocksworld-4ops)
(:objects a b c d e )
(:init
(handempty)
(on a d)
(ontable b)
(on c e)
(ontable d)
(on e b)
(clear a)
(clear c)
)
(:goal
(and
(on a c)
(on b a)
(on d b)
(on e d))
)
)


