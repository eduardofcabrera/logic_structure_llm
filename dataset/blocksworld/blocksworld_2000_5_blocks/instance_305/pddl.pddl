

(define (problem BW-rand-5)
(:domain blocksworld-4ops)
(:objects a b c d e )
(:init
(handempty)
(on a e)
(ontable b)
(on c a)
(on d c)
(on e b)
(clear d)
)
(:goal
(and
(on b a)
(on d b)
(on e d))
)
)


