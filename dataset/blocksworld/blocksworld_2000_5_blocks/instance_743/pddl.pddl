

(define (problem BW-rand-5)
(:domain blocksworld-4ops)
(:objects a b c d e )
(:init
(handempty)
(on a e)
(on b d)
(on c a)
(ontable d)
(on e b)
(clear c)
)
(:goal
(and
(on a d)
(on b a)
(on d c)
(on e b))
)
)


