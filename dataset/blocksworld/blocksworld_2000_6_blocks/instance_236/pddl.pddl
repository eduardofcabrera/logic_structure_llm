

(define (problem BW-rand-5)
(:domain blocksworld-4ops)
(:objects a b c d e )
(:init
(handempty)
(ontable a)
(on b a)
(on c d)
(on d e)
(on e b)
(clear c)
)
(:goal
(and
(on a b)
(on c a)
(on d c))
)
)


